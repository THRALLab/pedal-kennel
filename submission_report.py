import json
import os
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, inspect, select
from pedal.core.submission import Submission
from pedal.core.commands import contextualize_report

# Database path
db_path = 'sqlite:////Users/elizabethdassoulas/Desktop/VIP/v3.db'

# To create database engine
engine = create_engine(db_path)

# Use an inspector to get table names
inspector = inspect(engine)
table_names = inspector.get_table_names()

# To print all table names
print("Tables in the database:", table_names)

# Chose LinkAssignment as my table to work with
table_name = 'LinkAssignment'

# To reflect the selected table
metadata = MetaData()
table = Table(table_name, metadata, autoload_with=engine)
print(table.columns)


def fetch_latest_submission():
    """Retrieve the most recent student submission from the database."""
    with engine.connect() as conn:
        query = select(table).order_by(table.c.AssignmentID.desc()).limit(1)
        result = conn.execute(query).fetchone()

        if result:
            # Print the result to inspect available data
            print("Query result:", result)

            assignment_id = result[0]  # AssignmentID
            assignment_name = result[2]  # Name (assignment name)
            instructions = result[6]  # Instructions (perhaps it's used as a description)

            # For now, let's use "instructions" as part of the contextualization
            return {
                "assignment_id": assignment_id,
                "assignment_name": assignment_name,
                "instructions": instructions,  # Add instructions or other relevant fields
            }
    return None


def save_report_to_file(submission_data, contextualized_report):
    """Save the report and related metadata to a file in the submission_reports folder."""

    # Define the folder path
    folder_path = os.path.join(os.getcwd(), "submission_reports")

    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"report_{submission_data['assignment_name']}_{timestamp}.json"

    # Define the full path for saving the report
    file_path = os.path.join(folder_path, report_filename)

    # Create a dictionary to store the report and metadata
    report_content = {
        "assignment_name": submission_data["assignment_name"],
        "assignment_id": submission_data["assignment_id"],
        "instructions": submission_data["instructions"],
        "contextualized_report": contextualized_report,
        "query_used": f"SELECT * FROM {table_name} ORDER BY AssignmentID DESC LIMIT 1",  # Modify as needed
        "dataset_location": "LinkAssignment",  # Add more details if necessary
    }

    # Write report to the JSON file in the submission_reports folder
    with open(file_path, "w") as f:
        json.dump(report_content, f, indent=4)

    print(f"Report saved to {file_path}")

def contextualize_submission():
    """Fetch submission from the database, pass it to contextualize_report, and save the report to a file."""
    submission_data = fetch_latest_submission()

    if submission_data:
        # Use the retrieved assignment name and instructions
        print(f"Processing submission for {submission_data['assignment_name']}")

        # Placeholder for files
        files = {submission_data["assignment_name"]: submission_data["instructions"]}

        # Create a submission (adjust the keys)
        submission = Submission(files, user={"name": submission_data["assignment_name"]})

        # Contextualize the report with the submission
        contextualized_report = contextualize_report(submission)

        # Save the contextualized report and metadata to a file
        save_report_to_file(submission_data, contextualized_report)

        print(f"Submission for {submission_data['assignment_name']} has been contextualized.")
    else:
        print("No submission found in the database.")


if __name__ == "__main__":
    contextualize_submission()

