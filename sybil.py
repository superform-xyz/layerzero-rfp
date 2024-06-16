import pandas as pd
import requests
import time
import csv
import json

# Read the CSV file
csv_file = 'Superform_LZ_RFP_User_Allocation_Final.csv'
df = pd.read_csv(csv_file)

# Define the API URL
api_url = "https://wenser.xyz/api/layerzerosybil/final?address={}"

# Function to call the API with backoff retries
def call_api_with_backoff(address, max_retries=5, backoff_factor=0.5):
    for retry in range(max_retries):
        try:
            response = requests.get(api_url.format(address))
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Non-200 status code: {response.status_code}. Retrying...")
        except requests.RequestException as e:
            print(f"Request failed: {e}. Retrying...")

        time.sleep(backoff_factor * (2 ** retry))

    return None

# Create a list to store the results
results = []

# Iterate through each address in the DataFrame
for index, row in df.iterrows():
    address = row['Address']
    allocation = row['Allocation %']
    response = call_api_with_backoff(address)
    print(response)
    if response:
        is_sybil = response.get('isSybil', None)
        results.append({'Address': address, 'Allocation %': allocation, 'isSybil': is_sybil})
    else:
        results.append({'Address': address, 'Allocation %': allocation, 'isSybil': None})

# Write the results to a new CSV file
output_file = 'Superform_LZ_RFP_User_Allocation_Sybil_Results.csv'
with open(output_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Address', 'Allocation %', 'isSybil'])
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to {output_file}")
