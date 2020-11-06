# Part C: Finding the right amount to save away

# User input annual salary
salary = int(input("Enter starting salary: "))
 # Calculate the initial monthly salary
monthly_salary = float(salary/12)
# Cost of dream house
total_cost = 1000000
# Cost of down payment
down_payment = 1000000 * 0.25
# Initializing number of steps of binary search to 0
steps = 0
# Initializing semi annual raise
semi_annual_raise = 0.07
# Initializing returns
r = 0.04
# Initializing lower boundary of binary search
low = 0
# Initializing upper boundary of binary search
high = 10000
# Initializing number of months as 0
counter = 0
counter_1 = 0
# Initializing the saving rate 
saving_rate = 0
# Initializing total savings
total_savings = float(0)
# Checking is saving all the salary will be less than the downpayment
for i in range(36):
    counter = counter + 1
    if counter % 6 == 0:
        monthly_salary = round(monthly_salary * (1 + semi_annual_raise), 2)
    total_savings = round(total_savings + (monthly_salary * 1) + ((total_savings * r )/ 12),2)  
if total_savings < down_payment:
    counter_1 = 1
    print("It is not possible to pay for the downpayment in 3 years")
# Looping until a suitable saving rate is found
while abs(total_savings - down_payment) >= 100:
    if counter_1 == 1:
        break
    # Reseting appropriate varibales
    total_savings = 0.00
    counter = 0
    monthly_salary = round(float(salary/12),2)
    saving_rate = round(float((low + high) / 20000),4)
    for i in range(36):
        counter = counter + 1
        # Afer every 6th months salary will increase
        if counter % 6 == 0:
            monthly_salary = round(monthly_salary * (1 + semi_annual_raise), 2)
        total_savings = round(total_savings + (monthly_salary * saving_rate) + ((total_savings * r )/ 12),2)  
    # Search upper half if savings less than downpayment    
    if total_savings < down_payment:
        low = int(saving_rate * 10000)
    # Search lower half if savings more than downpayment    
    else:  
        high = int(saving_rate * 10000)
    steps = steps + 1
if counter_1 == 0:    
    print(f"steps: {steps}")
    print(f"saving rate: {saving_rate}")      
    print(f"total savings: {total_savings}")                      