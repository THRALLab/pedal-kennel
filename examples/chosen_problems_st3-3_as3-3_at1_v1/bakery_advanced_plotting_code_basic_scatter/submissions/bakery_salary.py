from dataclasses import dataclass

@dataclass
class Industry:
    """
    Information about an individual industry.
    
    Attributes:
        name: The name of the industry
        members: The number of people employed in the industry.
        mean_salary: The average salary of people in this industry.
        median_salary: The median salary of people in this industry (more robust to outliers).
    """
    name: str
    members: int
    mean_salary: int
    median_salary: int

industries = []
with open('raw_salaries.csv') as salary_file:
    for line in salary_file:
        name, members, mean, median = line.split("|")
        industries.append(Industry(
            name, int(members), int(mean), int(median)
        ))
