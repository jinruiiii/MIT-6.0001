# Part A: House hunting
annual_salary = float(input("Input Annual Salary: "))
portion_saved = float(input("Portion to be saved: "))
total_cost = float(input("Cost of your dream home: "))
portion_down_payment = 0.25 * total_cost
current_savings = float(0)
monthly_salary = annual_salary / 12
counter = 0
r = 0.04
while current_savings < portion_down_payment:
    current_savings = current_savings + (monthly_salary * portion_saved) + ((current_savings * r) / 12) 
    counter = counter + 1
print(counter)   