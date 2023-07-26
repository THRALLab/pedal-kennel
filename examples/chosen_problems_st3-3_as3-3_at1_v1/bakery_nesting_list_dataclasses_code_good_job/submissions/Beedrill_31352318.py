from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str
    
UNEMPLOYED = Job("Unemployed", 0, True, "None")

def best_job(jobs: [Job]) -> Job:
    if not [job for job in jobs if job.available]:
        return UNEMPLOYED
    return max([job for job in jobs if job.available], key=lambda job: job.salary)

