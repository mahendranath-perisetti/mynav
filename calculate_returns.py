import json
from pathlib import Path

INPUT_FILE = Path('data.json')
OUTPUT_FILE = Path('returns.json')

# If your data.json values are total AUM, set shares_outstanding here.
# For example, if the fund has 10,000 outstanding shares, set 10000.
shares_outstanding = 13.0

with INPUT_FILE.open('r') as f:
    data = json.load(f)

if not data:
    raise ValueError('data.json is empty or invalid')

# Use `aum` if provided; otherwise fall back to `value`.
first_entry = data[0]
aum_key = 'aum' if 'aum' in first_entry else 'value'
initial_aum = first_entry.get(aum_key)

if initial_aum is None:
    raise ValueError('Each entry in data.json must include either "aum" or "value"')

returns_data = []
for entry in data:
    date = entry['date']
    aum = entry.get(aum_key)
    if aum is None:
        raise ValueError(f'Entry for {date} is missing "{aum_key}"')

    nav = aum / shares_outstanding
    percentage_return = ((nav - (initial_aum / shares_outstanding)) / (initial_aum / shares_outstanding)) * 100

    returns_data.append({
        'date': date,
        'aum': aum,
        'nav': round(nav, 2),
        'percentage_return': round(percentage_return, 2)
    })

print('Date\t\tAUM\t\tNAV\t\tPercentage Return (%)')
print('-' * 70)
for entry in returns_data:
    print(f"{entry['date']}\t{entry['aum']}\t{entry['nav']}\t\t{entry['percentage_return']}")

with OUTPUT_FILE.open('w') as f:
    json.dump(returns_data, f, indent=2)

print('\nResults saved to returns.json')