from bakery_salary import industries
import matplotlib.pyplot as plt

mean_salaries = [industry.mean_salary for industry in industries]
median_salaries = [industry.median_salary for industry in industries]
members_list = [industry.members for industry in industries]

plt.scatter(mean_salaries, median_salaries, label="Mean vs Median Salary")
plt.scatter(mean_salaries, members, label="Mean Salaries vs Member Count")
plt.xlabel("Mean Salary")
plt.legend()
plt.show()