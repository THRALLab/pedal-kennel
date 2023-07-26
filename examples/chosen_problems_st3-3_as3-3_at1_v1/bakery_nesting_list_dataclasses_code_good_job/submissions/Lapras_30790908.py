from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str
    
UNEMPLOYED = Job("Unemployed", 0, True, "None")

def best_job(jobs:[Job])-> Job:
    greatest_job = UNEMPLOYED.salary
    for job in jobs:
        if job.salary > greatest_job:
            if job.available:
                greatest_job = job.salary
    return greatest_job

jobslist = [Job('Legend', 0, False, 'Earth'),
            Job('Garbageman', 30_000, True, 'City'),
            Job('Lawyer', 400_000, False, 'City'),
            Job('Plumber', 75_000, True, 'City')]
assert_equal(best_job(jobslist), 75_000)
assert_equal(best_job([]), 0)
assert_equalassert_equal(best_job(jobslist[:-1]), 30_000)