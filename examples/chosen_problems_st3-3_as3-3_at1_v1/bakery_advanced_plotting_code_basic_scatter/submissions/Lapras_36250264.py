from bakery_salary import industries
import matplotlib.pyplot as plt
members = []
mean = []
median = []
for industry in industries:
    members.append(industry.members)
    mean.append(industry.mean_salary)
    median.append(industry.median_salary)
plt.scatter(mean, median)
plt.title('Mean vs Median')
plt.ylabel('Median')
plt.xlabel('Mean')
plt.show()
plt.scatter(mean, members)
plt.title('Mean vs Members')
plt.ylabel('Members')
plt.xlabel('Mean')
plt.show()
