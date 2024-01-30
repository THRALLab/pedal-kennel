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
    highestPay = 0
    jobTitle = ""
    for job in jobs:
        if job.available == False:
            if job.salary > highestPay:
                highestPay = job.salary
                jobTitle = job.title
    return jobTitle