from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Job:
    title: str
    salary: int
    available: bool
    company: str
    
UNEMPLOYED = Job("Unemployed", 0, True, "None")

