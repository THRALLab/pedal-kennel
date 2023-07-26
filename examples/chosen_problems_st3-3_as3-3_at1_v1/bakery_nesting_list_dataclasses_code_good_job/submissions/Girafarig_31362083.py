from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str
    
UNEMPLOYED = Job("Unemployed", 0, True, "None")

def best_job(jobs: list[Job]) -> Job:
    greatest_job = UNEMPLOYED
    for job in jobs:
        if job.available:
            if job.salary > greatest_job.salary:
                greatest_job = job
    return greatest_job


painter = Job("Painter", 5000, True, "Painers Inc.")
seamstress = Job("Seamstress", 4000, False, "Sewing and Strings")
server = Job("waiter", 3500, False, "Bob's")

assert_equal(best_job([painter, seamstress, waiter]), 8500)
assert_equal(best_job([waiter]), UNEMPLOYED)
assert_equal(best_job([painter]), 5000)

