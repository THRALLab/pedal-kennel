from bakery_salary import industries
import matplotlib.pyplot as plt

mean_salary_list=[]
for industry in industries:
    mean_salary_list.append(industry.mean_salary/1000)
median_salary_list=[]
for industry in industries:
    median_salary_list.append(industry.median_salary)
members_list=[]
for industry in industries:
    members_list.append(industry.members)
plt.scatter(mean_salary_list, median_salary_list)
plt.xlabel("Mean Salary")
plt.ylabel("Median Salary")
plt.title("Mean Salary Compared to Median Salary")
plt.show
plt.scatter(mean_salary_list, members)
plt.xlabel("Mean Salary")
plt.ylabel("Members")
plt.title("Mean Salary Compared to Members")
plt.show

    
