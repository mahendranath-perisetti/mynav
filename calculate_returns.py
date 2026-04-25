import json

# Load the data from data.json
with open('data.json', 'r') as f:
    data = json.load(f)

# Assuming the first value is the initial NAV
initial_value = data[0]['value']

# Calculate percentage returns
returns_data = []
for entry in data:
    date = entry['date']
    value = entry['value']
    percentage_return = ((value - initial_value) / initial_value) * 100
    returns_data.append({
        'date': date,
        'nav': value,
        'percentage_return': round(percentage_return, 2)
    })

# Print the results
print("Date\t\tNAV\t\tPercentage Return (%)")
print("-" * 50)
for entry in returns_data:
    print(f"{entry['date']}\t{entry['nav']}\t\t{entry['percentage_return']}")

# Optionally, save to a new file
with open('returns.json', 'w') as f:
    json.dump(returns_data, f, indent=2)

print("\nResults saved to returns.json")