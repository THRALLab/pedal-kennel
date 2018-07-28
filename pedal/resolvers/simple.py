from pedal.report import MAIN_REPORT

DEFAULT_CATEGORY_PRIORITY = [
    'syntax',
    'analyzer',
    'mistakes',
    'runtime',
    'instructor',
    'uncategorized'
]

# For compatibility with the old feedback API
LEGACY_CATEGORIZATIONS = {
    'student': 'runtime',
    'parser': 'syntax',
    'verifier': 'syntax',
    'instructor': 'instructor'
}

def by_priority(feedback):
    '''
    Converts a feedback into a numeric representation for sorting.
    
    Args:
        feedback (Feedback): The feedback object to convert
    Returns:
        float: A decimal number representing the feedback's relative priority.
    '''
    category = 'uncategorized'
    if feedback.category is not None:
        category = feedback.category.lower()
    priority = 'medium'
    if feedback.priority is not None:
        priority = feedback.priority.lower()
        priority = LEGACY_CATEGORIZATIONS.get(priority, priority)
    if category in DEFAULT_CATEGORY_PRIORITY:
        value = DEFAULT_CATEGORY_PRIORITY.index(category)
    else:
        value = len(DEFAULT_CATEGORY_PRIORITY)
    offset = .5
    if priority == 'low':
        offset = .3
    elif priority == 'high':
        offset = .7
    elif priority not in ('low', 'medium', 'high'):
        if priority in DEFAULT_CATEGORY_PRIORITY:
            value = DEFAULT_CATEGORY_PRIORITY.index(priority)
            offset = .1
    return value + offset

def parse_message(component):
    if isinstance(component, str):
        return component
    elif isinstance(component, list):
        return '<br>\n'.join(parse_component(c) for c in component)
    elif isinstance(component, dict):
        if "html" in component:
            return component["html"]
        elif "message" in component:
            return component["message"]
        else:
            raise ValueError("Component has no message field: "+str(component))
    else:
        raise ValueError("Invalid component type: "+str(type(component)))

def parse_data(component):
    if isinstance(component, str):
        return [{'message': component}]
    elif isinstance(component, list):
        return component
    elif isinstance(component, dict):
        return [component]

MESSAGE_TYPES = ['hints', 'mistakes', 'misconceptions', 
                 'constraints', 'metacognitives']
def parse_feedback(feedback):
    # Default returns
    success = False
    performance = 0
    message = None
    data = []
    # Actual processing
    for feedback_type in MESSAGE_TYPES:
        feedback_value = getattr(feedback, feedback_type)
        if feedback_value is not None:
            data.extend(parse_data(feedback_value))
            parsed_message = parse_message(feedback_value)
            if parsed_message is not None:
                message = parsed_message
    if feedback.result is not None:
        success = feedback.result
    if feedback.performance is not None:
        performance = feedback.performance
    return success, performance, message, data

'''
    if (!suppress['parser'] && !report['parser'].success) {
        var parserReport = report['parser'].error;
        this.convertSkulptSyntax(parserReport);
        return 'parser';
    }
    // Error in Instructor Feedback code
    if (!report['instructor'].success) {
        this.presentInstructorError();
    }
    if (report['instructor'].compliments && report['instructor'].compliments.length) {
        //this.compliment(report['instructor'].compliments);
        console.log(report['instructor'].compliments);
    }
    if (suppress['instructor'] !== true && complaint && complaint.length) {
        complaint.sort(BlockPyFeedback.sortPriorities);
        this.instructorFeedback(complaint[0].name, complaint[0].message, complaint[0].line);
        return 'instructor';
    }
    // Analyzer
    if (!report['instructor'].hide_correctness &&
        suppress['analyzer'] !== true) {//if a subtype is specified, or no suppression requested, present feedback
        if (!report['analyzer'].success) {
            this.internalError(report['analyzer'].error, "Analyzer Error", "Error in analyzer. Please show the above message to an instructor!");
            return 'analyzer';
        }
        var wasPresented = this.presentAnalyzerFeedback();
        if (wasPresented) {
            return 'analyzer';
        }
    }
    // Student runtime errors
    if (!suppress['student']) {
        if (!report['student'].success) {
            this.printError(report['student'].error);
            return 'student';
        }
    }
    // No instructor feedback if hiding correctness
    if (report['instructor'].hide_correctness == true) {
        this.noErrors()
        return 'no errors';
    }
    // Gentle instructor feedback
    if (suppress['instructor'] !== true && gentleComplaints.length) {
        this.instructorFeedback(gentleComplaints[0].name, 
                                gentleComplaints[0].message, 
                                gentleComplaints[0].line);
        return 'instructor';
    }
    //instructor completion flag
    if (suppress['instructor'] !== true && report['instructor'].complete) {
        this.complete();
        return 'success';
    }
    if (!suppress['no errors']) {
        this.noErrors()
        return 'no errors';
    }
    return 'completed';
'''

def resolve(report=None, priority_key=None):
    '''
    Args:
        report (Report): The report object to resolve down. Defaults to the
                         global MAIN_REPORT
    
    Returns
        str: A string of HTML feedback to be delivered
    '''
    if report is None:
        report = MAIN_REPORT
    if priority_key is None:
        priority_key = by_priority
    # Prepare feedbacks
    feedbacks = report.feedback
    feedbacks.sort(key=by_priority)
    suppressions = report.suppressions
    # Process
    final_success = False
    final_score = 0
    final_message = None
    final_category = "Instructor"
    final_label = ""
    final_data = None
    for feedback in feedbacks:
        if feedback.category in suppressions:
            if True in suppressions[feedback.category]:
                continue
            elif feedback.label in suppressions[feedback.category]:
                continue
        success, partial, message, data = parse_feedback(feedback)
        final_success = success or final_success
        final_score += partial
        if message is not None and final_message is None:
            final_message = message
            final_category = feedback.category
            final_label = feedback.label
            final_data = data
    if final_message is None:
        final_message = "No errors reported."
    return (final_success, final_score, final_category, 
            final_label, final_message, final_data)
