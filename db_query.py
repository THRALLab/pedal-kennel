import os
from sqlalchemy import create_engine, MetaData, Table, select, and_, func
from pedal.core.submission import Submission
from pedal.core.commands import contextualize_report

# Database path
db_path = 'sqlite:////Users/u001m/BlockPyProject/sample_data_spring_2025.db'
engine = create_engine(db_path)

# Reflect tables
metadata = MetaData()
main_table = Table('MainTable', metadata, autoload_with=engine)
code_state = Table('CodeState', metadata, autoload_with=engine)
link_assignment = Table('LinkAssignment', metadata, autoload_with=engine)

# Directory to save files (can be customized)
output_dir = "output_code"
os.makedirs(output_dir, exist_ok=True)

# put the assignment_id you want to pull here
assignment_id = "bakery_intro_string_ops_code_string_tests";


def fetch_custom_submission():
    """Fetch a specific submission and save student/instructor code to files."""
    with engine.connect() as conn:
        query = (
            select(code_state.c.Contents, link_assignment.c.CodeOnRun)
            .select_from(
                main_table
                .join(code_state, main_table.c.CodeStateID == code_state.c.CodeStateID)
                .join(link_assignment, main_table.c.AssignmentID == link_assignment.c.AssignmentID)
            )
            .where(
                and_(
                    main_table.c.AssignmentID == assignment_id,
                    func.length(code_state.c.Contents) != 0,
                    func.length(link_assignment.c.CodeOnRun) != 0
                )
            )
        )

        result = conn.execute(query).fetchone()

        if result:
            student_code = result.Contents
            instructor_code = result.CodeOnRun

            # Save to files
            student_file_path = "examples/submissions/unused.py"
            instructor_file_path = "examples/blank_instructor.py"

            with open(student_file_path, "w", encoding="utf-8") as f:
                f.write(student_code)
            with open(instructor_file_path, "w", encoding="utf-8") as f:
                f.write(instructor_code)

            print(f"Student code written to: {student_file_path}")
            print(f"Instructor code written to: {instructor_file_path}")

            return {
                "assignment_name": assignment_id,
                "contents": student_code,
                "code_on_run": instructor_code
            }

    return None

fetch_custom_submission()