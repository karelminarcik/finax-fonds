from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime

list_of_fonds = ["SXR8:GR", "SPY4:GR", "ZPRR:GR", "IS3N:GR", "XSX6:GR", "XXSC:GR"]

def date():
    current_date = datetime.now().date()
    current_date_str = current_date.strftime("%d-%m-%Y")
    return current_date_str

def chrom_driver():
    # Set Chrome options to suppress log messages
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--log-level=3")  # Suppresses warning and error messages

    # Initialize the Chrome driver with options
    driver = webdriver.Chrome(options=chrome_options)
    return(driver)

def find_fonds(driver,fonds):
    for fond in fonds:
        try:
            # Open the Bloomberg quote page
            driver.get(f"https://www.bloomberg.com/quote/{fond}")

            # Wait for the fond value element to be present and get its text
            fond_value = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".media-ui-SizedPrice_extraLarge-05pKbJRbUH8-"))
            ).text
            print(fond_value)

            write_to_csv(fond, fond_value)

        except Exception as e:
            print(f"{fond} not found: ", e)


def write_to_csv(fond, fond_value):
    # Write the data to a CSV file
        csv_filename = f"{fond}.csv"
        csv_filename = csv_filename.replace(":", "_")
        with open(csv_filename, "a", newline='') as data:
            writer = csv.writer(data)
            # writer.writerow(["Datum", "Vykonnost fondu"]) #not needed anymore
            writer.writerow([date, fond_value])
        print(f"Data written to {csv_filename}")
    


if __name__ == "__main__":
    date = date()
    driver = chrom_driver()

    find_fonds(driver, list_of_fonds)

    # Close the driver after completing the operations
    driver.quit()