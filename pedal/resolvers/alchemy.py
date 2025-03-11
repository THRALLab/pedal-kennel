import json
from pedal.core.report import MAIN_REPORT
from pedal.core.final_feedback import FinalFeedback, set_correct_no_errors, deserialize_final_feedback
from pedal.core.feedback import Feedback, DEFAULT_CATEGORY_PRIORITY
from pedal.resolvers.export import PedalJSONEncoder, clean_json
from pedal.resolvers.core import make_resolver
from pedal.resolvers.simple import by_priority


# commented out by Olivia - seems like this is not complete yet and its causing errors
#import requests


@make_resolver
def resolve(report=MAIN_REPORT, priority_key=by_priority):
    """
    Args:
        priority_key: The key function to sort feedbacks by
        report (Report): The report object to resolve down. Defaults to the
                         global MAIN_REPORT

    Returns
        str: A string of HTML feedback to be delivered
    """

    # Prepare feedbacks
    feedbacks = report.feedback + report.ignored_feedback
    feedbacks.sort(key=priority_key)
    # Create the initial final feedback
    final = set_correct_no_errors(report)
    # Process each feedback in turn
    used = []
    for feedback in feedbacks:
        partial = final.merge(feedback)
        if partial is not None:
            used.append(partial)

    # final_data = final.to_json() - final data got replaced by report_data
    #print(report)
    #print(used)

    report_data = report.to_json()
    #print(report_data)

    parsed_data = json.loads(report_data)

    with open('final_data.json', 'w') as file:
        json.dump(parsed_data, file, indent=4)

    # commented out by olivia because we are not using it yet
    '''
    # Send the report to the server
    try:
        response = requests.post("http://localhost:8000/", json=final_data)
        if response.status_code == 200:
            server_result = response.json()
            # Deserialize the server result into a FinalFeedback object
            final = deserialize_final_feedback(json.dumps(server_result))
            print("Deserialized FinalFeedback:", final)
        else:
            print("Failed to get a valid response from the server:", response.status_code)
    except requests.ConnectionError:
        print("Failed to connect to the server")
    '''
    # Not sure if you would want to make Alchemy's return a Feedback item so it can be added to result or something else entirely.
    # Override empty message
    final.finalize()
    final.used = used
    report.result = final
    report.resolves.append(final)
    return final
