from sqlalchemy import create_engine, MetaData, Table, inspect, select
from pedal.core.submission import Submission
from pedal.core.commands import contextualize_report

#database path
db_path = 'sqlite:////Users/elizabethdassoulas/Desktop/VIP/v3.db'

#to create database engine
engine = create_engine(db_path)

# Use an inspector to get table names
inspector = inspect(engine)
table_names = inspector.get_table_names()

# To rint all table names
print("Tables in the database:", table_names)

#Chose LinkAssignment as my table to work with
table_name = 'LinkAssignment'

# To reflect the selected table
metadata = MetaData()
table = Table(table_name, metadata, autoload_with=engine)
print(table.columns)



# Query data from table
#with engine.connect() as conn:
 #   result = conn.execute(table.select()).fetchall()
 #   for row in result:
 #       print(row)


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

            # For now, let's use "instructions" as part of the contextualization, or whatever makes sense
            return {
                "assignment_id": assignment_id,
                "assignment_name": assignment_name,
                "instructions": instructions,  # Add instructions or other relevant fields
            }
    return None


def contextualize_submission():
    """Fetch submission from the database and pass it to contextualize_report."""
    submission_data = fetch_latest_submission()

    if submission_data:
        # Use the retrieved assignment name and instructions, or modify to suit your needs
        print(f"Processing submission for {submission_data['assignment_name']}")

        # Placeholder for files
        files = {submission_data["assignment_name"]: submission_data["instructions"]}

        # Create a submission (you may need to adjust the keys)
        submission = Submission(files, user={"name": submission_data["assignment_name"]})

        # Contextualize the report with the submission
        contextualize_report(submission)
        print(f"Submission for {submission_data['assignment_name']} has been contextualized.")
    else:
        print("No submission found in the database.")
