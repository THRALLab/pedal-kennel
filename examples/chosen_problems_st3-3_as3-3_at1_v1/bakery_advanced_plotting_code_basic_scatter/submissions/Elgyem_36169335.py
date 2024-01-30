from bakery_salary import industries
import matplotlib.pyplot as plt

mean=[]
median=[]
number=[]
for industry in industries:
    mean.append(industry.mean_salary)
    median.append(industry.median_salary)
    number.append(industry.members)
        
plt.scatter(mean,median)
plt.xlablel(mean_salary)
plt.ylablel(members)
plt.show()

plt.scatter(mean,number)
plt.xlablel=(mean_salary)
plt.ylablel=(median_salary)
plt.show()