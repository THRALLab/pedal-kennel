from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str
    
def available_jobs(jobs:list[Job])->list[job]:
    avail_jobs=[]
    for job in jobs:
        if job.available:
            avail_jobs.append(job)
    return avail_jobs

def highest_salary(jobs:list[Job])->int:
    maximum=jobs[0].salary
    for job in jobs:
        if maximum<job.salary:
            maximum=job.salary
    return maximum

UNEMPLOYED = Job("Unemployed", 0, True, "None")

def best_job(jobs:list[Job])->Job:
    x=available_jobs(jobs)
    if not x:
        return UNEMPLOYED
    y=highest_salary(x)
    for job in jobs:
        if job.salary==maximum:
            return job   
    

list1:[Job("Dancer", 5000, True, "None"),Job("Driver", 200, True, "None")]
list2:[Job("Painter",0, True, "None"),Job("Explorer", 200, False, "None")]
list3:[Job("Hooper", 1000, False, "None"),Job("Scientist", 1200, False, "None")]

assert_equal(best_job(list1), Job("Dancer", 5000, True, "None"))
assert_equal(best_job(list2), Job("Painter",0, True, "None"))
assert_equal(best_job(list3), UNEMPLOYED = Job("Unemployed", 0, True, "None"))