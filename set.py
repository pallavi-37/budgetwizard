import pandas as pd
import random
import faker

# Initialize the Faker library for generating random data
fake = faker.Faker()

# Common expense names (extended list)
expense_names = [
    "Groceries",
    "Rent",
    "Utilities",
    "Transportation",
    "Dining Out",
    "Entertainment",
    "Clothing",
    "Healthcare",
    "Education",
    "Insurance",
    "Home Mortgage",
    "Car Payment",
    "Gasoline",
    "Phone Bill",
    "Internet Bill",
    "Electricity Bill",
    "Water Bill",
    "Credit Card Payment",
    "Gym Membership",
    "Netflix Subscription",
    "Amazon Shopping",
    "Travel Expenses",
    "Medical Bills",
    "Home Repairs",
    "Tuition Fees",
    "Life Insurance",
    "Car Insurance",
    "Pet Expenses",
    "Gifts",
    "Hobbies",
    "Charity Donations",
    "Vacation",
    "Groceries",
    "Childcare",
    "Haircut",
    "Laundry",
    "Dental Checkup",
    "Property Taxes",
    "Investment",
    "Savings",
    "Loan Repayment",
    "Alcohol",
    "Cigarettes",
    "Coffee",
    "Restaurant",
    "Fast Food",
    "Snacks",
    "Books",
    "Magazines",
]


# Number of rows in the dataset
num_rows = 250

# Generate random data for the dataset
data = {
    'date': [fake.date_between(start_date='-30d', end_date='today') for _ in range(num_rows)],
    'expensename': [random.choice(expense_names) for _ in range(num_rows)],
    'amount': [random.randint(1, 1000) for _ in range(num_rows)],  # Generates random integers
    'paymode': [random.choice(['cash', 'creditcard', 'debitcard', 'epayment','onlinebanking']) for _ in range(num_rows)],
    'category': [random.choice(['food', 'EMI', 'Entertainment', 'Rent', 'other','Business']) for _ in range(num_rows)],
}

# Ensure that all data lists have the same length (num_rows)
assert len(data['date']) == len(data['expensename']) == len(data['amount']) == len(data['paymode']) == len(data['category']) == num_rows

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Display the first few rows of the dataset
print(df.head())

# Save the dataset to a CSV file
df.to_csv('expensedata4.csv', index=False)
