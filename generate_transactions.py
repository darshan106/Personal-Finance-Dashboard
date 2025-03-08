import csv
import random
from datetime import datetime, timedelta
from calendar import monthrange

# Helper function to generate random dates for each month
def generate_dates_for_month(year, month):
    num_days = monthrange(year, month)[1]  # Get the number of days in the month
    dates = []
    for day in range(1, num_days + 1):
        current_date = datetime(year, month, day)
        dates.append(current_date.strftime('%d-%m-%Y'))  # Format to DD-MM-YYYY
    return dates

# List of sample restaurant names, supermarket names, etc., specific to Bangalore
restaurants = [
    "Toit", "MTR 1924", "Corner House", "Olive Beach", "The Permit Room", "The Fatty Bao", 
    "Koshy's", "Barbecue Nation", "Truffles", "Chai Point"
]

supermarkets = [
    "Big Bazaar", "More Supermarket", "Spencer's", "Reliance Fresh", "Foodworld", "Easyday"
]

streaming_services = [
    "Netflix", "Amazon Prime", "Disney+ Hotstar", "Zee5"
]

gym_services = [
    "Cult.Fit"
]

# Helper function to generate the data based on the pattern
def generate_data():
    # Start date (January 2023)
    start_date = datetime(2023, 1, 1)
    
    # Transaction names and types
    transaction_patterns = [
        ('Software Engineer', 'Income', 75000),
        ('Dream Apartment', 'Expense', 28000),
        ('Electricity Bill', 'Expense', 1500),
        ('Water Bill', 'Expense', 500),
        ('Website Design', 'Income', 15000),
        ('ACT Fibernet', 'Expense', 1500),
        ('Netflix', 'Expense', 800),
        ('Cult.Fit', 'Expense', 2000),
        ('PVR Cinemas', 'Expense', 1200)
    ]
    
    # Initialize the result data list
    data = [['Date', 'Transaction Names', 'Transaction Type', 'Amount (INR)']]
    
    # Generate data for 24 months (Jan 2023 to Dec 2024)
    for year in range(2023, 2025):
        for month in range(1, 13):
            # Generate random dates for each month
            month_dates = generate_dates_for_month(year, month)
            
            # Randomize restaurant and supermarket names for each month
            restaurant = random.choice(restaurants)
            supermarket = random.choice(supermarkets)
            streaming_service = random.choice(streaming_services)
            gym_service = random.choice(gym_services)
            
            # Assign a unique date to each transaction
            monthly_transactions = [
                [random.choice(month_dates), "Software Engineer", "Income", 75000],
                [random.choice(month_dates), "Dream Apartment", "Expense", 28000],
                [random.choice(month_dates), "Electricity Bill", "Expense", 1500],
                [random.choice(month_dates), "Water Bill", "Expense", 500],
                [random.choice(month_dates), supermarket, "Expense", random.randint(2500, 4000)],  # Supermarket
                [random.choice(month_dates), restaurant, "Expense", random.randint(1500, 4000)],  # Restaurant
                [random.choice(month_dates), streaming_service, "Expense", 800],  # Streaming
                [random.choice(month_dates), gym_service, "Expense", random.randint(1800, 2500)],  # Gym
                [random.choice(month_dates), "Website Design", "Income", 15000],
                [random.choice(month_dates), "ACT Fibernet", "Expense", 1500],
                [random.choice(month_dates), "PVR Cinemas", "Expense", random.randint(1000, 1500)],  # Entertainment
            ]
            
            # Add the transactions of the month to the data
            data.extend(monthly_transactions)
    
    # Sort the data by date (DD-MM-YYYY format)
    data[1:] = sorted(data[1:], key=lambda x: datetime.strptime(x[0], "%d-%m-%Y"))
    
    return data

# Function to write the generated data into a CSV file
def write_to_csv(filename):
    data = generate_data()
    
    # Write the data to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"CSV file '{filename}' has been generated successfully!")

# Call the function to create the CSV
write_to_csv("Transactions_2023-24.csv")