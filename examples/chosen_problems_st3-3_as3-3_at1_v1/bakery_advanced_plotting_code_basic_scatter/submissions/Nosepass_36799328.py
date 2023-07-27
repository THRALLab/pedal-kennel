from bakery_salary import industries
import matplotlib.pyplot as plt

mean_sal = []
med_sal = []
members = []
for industry in industries:
    mean_sal.append(industry.mean_salary)
    med_sal.append(industry.med_sal)
    members.append(industry.members)
    
plt.scatter(mean_sal, med_sal)
plt.title('Mean and Median Salaries (U.S. DOL 2021)')
plt.xlabel('Mean Salary')
plt.ylabel('Median Salary')
plt.show()

plt.scatter(mean_sal, Members)
plt.title('Mean and Memebers Salaries (U.S. DOL 2021)')
plt.xlabel('Mean Salary')
plt.ylabel('Number of Members')
plt.show()