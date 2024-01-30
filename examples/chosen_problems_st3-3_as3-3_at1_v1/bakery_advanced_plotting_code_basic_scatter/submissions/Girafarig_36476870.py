from bakery_salary import industries

mean_salaries = []
median_salaries = []
for industry in industries:
    mean_salaries.append(industry.mean_salary)
    median_salaries.append(industry.median_salaries)

plt.scatter(mean_salaries, median_salaries)
plt.show()

plt.scatter(median_salaries, mean_salaries)
plt.show()