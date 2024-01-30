from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str
    
def filter_un(Jobs: list[Job])->list[Job]:
    avalible_jobs = []
    for job in Jobs:
        if job.avalible:
            avalible_jobs.append(job)
    return avalible_jobs

def best_job(Jobs: list[Job])->Job:
    largest_salary = 0
    filtered_jobs = filter_un(Jobs)
    
    if not filtered_jobs:
        return Job("Unemployed", 0, True, "None")
    
    best_job = filtered_jobs[0]
    for job in Jobs:
        if job.salary > best_job.slary:
            best_job = job
    return best_job

assert_equal(best_job([Job("Unemployed", 0, True, "None"),Job("Software Developer", 500000, False, "Google"),Job("TA",5,True,"Uni")]),Job("TA",5,True,"Uni"))
assert_equal(best_job([Job("Unemployed", 0, True, "None"),Job("Software Developer", 500000, True, "Google"),Job("TA",5,True,"Uni")]),Job("Software Developer", 500000, True, "Google"))
assert_equal(best_job([Job("Unemployed", 0, False, "None"),Job("Software Developer", 500000, False, "Google"),Job("TA",5,True,"Uni")]),Job("Unemployed", 0, True, "None"))
