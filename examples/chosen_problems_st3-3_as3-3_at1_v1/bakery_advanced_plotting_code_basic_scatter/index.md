Let us return to the salary data we saw a few problems ago. Previously, we looked at the distribution of the `mean_salary` data. Now we will compare that data with the `median_salary` data and then the `members` data to see if there are any correlations. Create *two* visualizations:

1. The first should show the relationship between `mean_salary` (x-axis) and `median_salary` (y-axis)
2. The second should show the relationship between `mean_salary` (x-axis) and `members` (y-axis)

Make sure you give meaningful labels to the axes and a title.

You are provided the following code in the `bakery_salary.py` file. Assume `raw_salaries.csv` is a valid CSV file:

```python
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
```
