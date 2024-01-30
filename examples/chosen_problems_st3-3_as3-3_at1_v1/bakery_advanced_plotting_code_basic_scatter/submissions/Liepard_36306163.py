from bakery_salary import industries

import matplotlib.pyplot as plt

totalMS = []
for industry in industries:
    totalMS.append(industry.mean_salary / 1000)
    
plt.hist(totalMS)
plt.xlabel("Mean Salary ($)")
plt.ylabel("Industries")
plt.title("Mean Salary of Industries")
plt.show()