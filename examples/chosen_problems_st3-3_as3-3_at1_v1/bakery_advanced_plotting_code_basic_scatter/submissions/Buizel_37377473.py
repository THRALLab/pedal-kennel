from bakery_salary import industries

import matplotlib.pyplot as plt


mean_salary = [50, 90, 150, 200, 250]

median_salary = [40, 80, 120, 180, 240]


plt.scatter(mean_salary, median_salary)

plt.xlabel('Mean Salary')

plt.ylabel('Median Salary')

plt.title('Relationship between Mean and Median Salary')

plt.show()