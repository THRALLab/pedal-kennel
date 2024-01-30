from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str
    
def can(have:list[Job])->bool:
    new_list=[]
    for h in have:
        if h.available==True:
            new_list.append(h)
    return new_list

def highest(
    
UNEMPLOYED = Job("Unemployed", 0, True, "None")

