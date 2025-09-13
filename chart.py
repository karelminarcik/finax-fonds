import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import os

def data_for_chart(file):
    # Read the CSV file
    data = pd.read_csv(file)

    # Ensure 'Datum' and 'Vykonnost_fondu' columns exist
    if 'Datum' not in data.columns or 'Vykonnost_fondu' not in data.columns:
        raise ValueError("The CSV file must contain 'Datum' and 'Vykonnost_fondu' columns.")

    # Convert the 'Datum' column to datetime for better handling
    data['Datum'] = pd.to_datetime(data['Datum'])

    # Extract the 'Datum' and 'Vykonnost_fondu' columns
    date_list = data['Datum'].to_list()
    vykonnost_list = data['Vykonnost_fondu'].to_list()

    return date_list, vykonnost_list

def plot_line_chart(file):
    # Get the data for the chart
    date_list, vykonnost_list = data_for_chart(file)

    # Extract the fund name from the file path
    fund_name = os.path.basename(file).split('.')[0]  # Get the file name without extension

    # Plotting the line chart
    plt.figure(figsize=(10, 6))
    plt.plot(date_list, vykonnost_list, color='blue', marker='o', linestyle='-', linewidth=2, markersize=4)

    # Customize the chart
    plt.xlabel('Date')
    plt.ylabel('Fund Performance')

    # Create two parts for the title, with different formatting for each
    title_text = f'Performance of the Fund {fund_name} Over Time. Latest Value: '
    latest_value = f'{vykonnost_list[-1]}'

    # Set title with bold font for latest_value
    plt.title(title_text + latest_value)

    # Format the date on the x-axis
    ax = plt.gca()

    # Set a major locator to space out date ticks (e.g., every 7 days)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))  # Change interval as needed

    # Set date format on the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Optionally, limit the number of ticks (if data is very dense)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=10))

    # Rotate date labels for better readability
    plt.xticks(rotation=45)

    # Set window title
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(f'{fund_name} Chart')

    # Display the chart
    plt.tight_layout()
    plt.show()

# Example usage
plot_line_chart('./SXR8_GR.csv')
