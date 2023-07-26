from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str
    
UNEMPLOYED = Job("Unemployed", 0, True, "None")

def available(avail:[Job])->bool:
    taking = []
    for avai in avail:
        if avail.available is True:
            taking.append(avai)
    return False

Job1 = [Job("banker", 5, True, "PNC")]
assert_equal(available(Job1), [Job("banker", 5, True, "PNC")])
