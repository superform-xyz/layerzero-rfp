import pandas as pd
import matplotlib.pyplot as plt

# Read the results CSV file
results_file = 'Superform_LZ_RFP_User_Allocation_Sybil_Results.csv'
df = pd.read_csv(results_file)

# Convert 'Allocation %' from a string with a percentage sign to a numeric value
df['Allocation %'] = df['Allocation %'].str.rstrip('%').astype(float)

# Sort the DataFrame by allocation %
df = df.sort_values(by='Allocation %', ascending=False)

# Initialize the cumulative allocation columns
df['cumulative_allocation_all'] = 0.0
df['cumulative_allocation_eligible'] = 0.0
cumulative_sum_all = 0.0
cumulative_sum_eligible = 0.0

# Iterate through the DataFrame and update the cumulative sum conditionally
for i, row in df.iterrows():
    cumulative_sum_all += row['Allocation %']
    if not row['isSybil']:
        cumulative_sum_eligible += row['Allocation %']
    df.at[i, 'cumulative_allocation_all'] = cumulative_sum_all
    df.at[i, 'cumulative_allocation_eligible'] = cumulative_sum_eligible

# Calculate cumulative eligible percentage
df['eligible_percentage'] = ((1 - df['isSybil']).expanding().mean() * 100).fillna(method='ffill')

# Plot the graph
fig, ax1 = plt.subplots()

# x-axis: order of addresses by allocation %
x = range(1, len(df) + 1)

# y-axis: percentage of addresses that are eligible and cumulative allocation eligible/all
ax1.set_xlabel('Order of Addresses by Allocation %')
ax1.set_ylabel('Percentage')
line2, = ax1.plot(x, df['eligible_percentage'], color='tab:red', label='% of Addresses that are Eligible')
line3, = ax1.plot(x, (df['cumulative_allocation_eligible'] / df['cumulative_allocation_all']) * 100, color='tab:green', label='Cumulative Allocation % (Eligible/All)')
ax1.tick_params(axis='y', labelcolor='tab:red')

# Add titles and legend
plt.title('Superform LayerZero Proposed RFP Eligibility')
fig.tight_layout()

# Annotate the last data point on each curve
last_index = len(df) - 1
ax1.annotate(f"{df['eligible_percentage'].iloc[last_index]:.2f}%",
             xy=(x[last_index], df['eligible_percentage'].iloc[last_index]),
             xytext=(5, 0), textcoords='offset points', color='tab:red')

ax1.annotate(f"{(df['cumulative_allocation_eligible'].iloc[last_index] / df['cumulative_allocation_all'].iloc[last_index] * 100):.2f}%",
             xy=(x[last_index], (df['cumulative_allocation_eligible'].iloc[last_index] / df['cumulative_allocation_all'].iloc[last_index] * 100)),
             xytext=(5, 0), textcoords='offset points', color='tab:green')

# Add legend
ax1.legend(loc='upper right')

# Show the plot
plt.show()
