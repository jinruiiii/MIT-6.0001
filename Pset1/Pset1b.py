# Part B: Saving with a raise

# Get user's annual salary, annual raise, portion to be saved and the total cost of the dream home
annual_salary = float(input("Input Annual Salary: "))
semi_annual_raise  = float(input("Semi-Annual Salary Raise: "))
portion_saved = float(input("Portion to be saved: "))
total_cost = float(input("Cost of your dream home: "))

# Calculate the required down payment
portion_down_payment = 0.25 * total_cost

# Initializing the curren savings as 0
current_savings = float(0)

# calculating the monthly salary
monthly_salary = annual_salary / 12

# Initializing the counter (number of months) to be 0
counter = 0

# Assigning the annual return as 0.04 per the question's instruction
r = 0.04

# Loop until currents savings is more than the down payment
while current_savings < portion_down_payment:
    counter = counter + 1
    if counter % 6 == 0:
        monthly_salary = monthly_salary * (1 + semi_annual_raise)
    current_savings = current_savings + (monthly_salary * portion_saved) + ((current_savings * r) / 12) 


# Printing the number of months required
print(counter)   