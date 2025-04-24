import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import os

# List of CSV files to include
files = ["SXR8_GR.csv", "SPY4_GR.csv", "ZPRR_GR.csv", "IS3N_GR.csv", "XSX6_GR.csv", "XXSC_GR.csv"]

def data_for_chart(file):
    # Read the CSV file
    data = pd.read_csv(file)

    # Ensure required columns exist
    if 'Datum' not in data.columns or 'Vykonnost_fondu' not in data.columns:
        raise ValueError(f"The CSV file {file} must contain 'Datum' and 'Vykonnost_fondu' columns.")
    
    # Convert the 'Datum' column to datetime
    data['Datum'] = pd.to_datetime(data['Datum'])
    
    return data[['Datum', 'Vykonnost_fondu']]

def plot_all_funds(files):
    plt.figure(figsize=(14, 8))  # Increase figure size for better readability
    fund_changes = []  # Store percentage changes for each fund
    
    for file in files:
        try:
            data = data_for_chart(file)
            fund_name = os.path.basename(file).split('.')[0]  # Extract fund name
            plt.plot(data['Datum'], data['Vykonnost_fondu'], marker='o', linestyle='-', label=fund_name, linewidth=2, markersize=5)
            
            # Annotate first and last values
            first_value = data['Vykonnost_fondu'].iloc[0]
            last_value = data['Vykonnost_fondu'].iloc[-1]
            plt.text(data['Datum'].iloc[0], first_value, f'{first_value:.2f}', fontsize=9, verticalalignment='bottom', color='black')
            plt.text(data['Datum'].iloc[-1], last_value, f'{last_value:.2f}', fontsize=9, verticalalignment='bottom', color='black')
            
            # Calculate percentage change
            percentage_change = ((last_value - first_value) / first_value) * 100
            fund_changes.append(f"{fund_name}: {percentage_change:.2f}%")
        except Exception as e:
            print(f"Skipping {file}: {e}")
    
    # Customize the chart
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Fund Performance', fontsize=12)
    plt.title('Performance of Multiple Funds Over Time', fontsize=14, fontweight='bold')
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    
    plt.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))  # Move legend outside plot
    plt.grid(True, linestyle='--', alpha=0.6)  # Add grid for better readability
    
    # Add percentage changes below legend
    plt.figtext(0.75, 0.2, "\n".join(fund_changes), fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    
    plt.tight_layout()
    plt.show()

# Plot all funds
plot_all_funds(files)
