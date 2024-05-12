import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import smtplib
from urllib.robotparser import RobotFileParser
import schedule
import time
import threading


def is_scraping_allowed(base_url, user_agent):
    rp = RobotFileParser()
    rp.set_url(base_url + "/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, base_url)


def scrape_and_save():
    # Specify the base URL of the website
    base_url = "https://www.ca.kayak.com"

    # Check if scraping is allowed
    if not is_scraping_allowed(base_url, "*"):
        messagebox.showerror("Error", "Scraping is not allowed as per robots.txt")
        return

    driver = webdriver.Chrome()
    departure_location = departure_entry.get()
    destination = destination_entry.get()
    departure_date = departure_date_entry.get()  # Example: "2024-07-01"
    arrival_date = arrival_date_entry.get()  # Example: "2024-07-31"
    
    url = f"https://www.ca.kayak.com/flights/{departure_location}-{destination}/{departure_date}/{arrival_date}?sort=bestflight_a"
    driver.get(url)
    sleep(5)
    flight_cards = driver.find_elements(By.XPATH, "//div[@class='nrc6 nrc6-mod-pres-default']")
    price_list = []
    company_name_list = []

    for WebElement in flight_cards:
        htmlElement = WebElement.get_attribute('outerHTML')
        soupElement = BeautifulSoup(htmlElement, 'html.parser')

        price = soupElement.find('div', {'class': 'f8F1-price-text'}).text
        price = price.replace('\xa0', '')
        price_list.append(price)

        company_name = soupElement.find('div', {'class': 'J0g6-operator-text'}).text
        company_name_list.append(company_name)

    df = pd.DataFrame({'Price': price_list, 'Company Name': company_name_list})

    # Save the DataFrame to a CSV file with timestamp
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(f'flight_data_{timestamp}.csv', index=False)

    # Update the message box with scraped data
    scraped_data_text.delete(1.0, tk.END)  # Clear previous data
    scraped_data_text.insert(tk.END, f"Flight data scraped successfully!\n\n{df}")

    # Send an email with the flight data
    email_sender(price_list, company_name_list)


def email_sender(price_list, company_name_list):
    message = f'Subject: Flight Data\n\nThe flight data has been scraped successfully\n\nPrice: {price_list}\nCompany Name: {company_name_list}'
    message = message.encode('utf-8')  # Encoding the message using UTF-8

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #Enter Your Own Email and Password
    server.login('Enter Yout Own Email', 'Enter Your Password')

    server.sendmail('Enter Yout Own Email', 'Enter Yout Own Email', message)


# Function to schedule scraping every two hours
def schedule_scraping():
    schedule.every(5).hours.do(scrape_and_save)

    while True:
        schedule.run_pending()
        time.sleep(1)


# GUI setup
root = tk.Tk()
root.title("Flight Scraper")
root.geometry("600x400")  # Set initial size of the window

departure_label = tk.Label(root, text="Departure Location:")
departure_label.grid(row=0, column=0, padx=10, pady=10)

departure_entry = tk.Entry(root)
departure_entry.grid(row=0, column=1, padx=10, pady=10)

destination_label = tk.Label(root, text="Destination:")
destination_label.grid(row=1, column=0, padx=10, pady=10)

destination_entry = tk.Entry(root)
destination_entry.grid(row=1, column=1, padx=10, pady=10)

departure_date_label = tk.Label(root, text="Departure Date (YYYY-MM-DD):")
departure_date_label.grid(row=2, column=0, padx=10, pady=10)

departure_date_entry = tk.Entry(root)
departure_date_entry.grid(row=2, column=1, padx=10, pady=10)
departure_date_entry.insert(0, "2024-07-01")  # Example date

arrival_date_label = tk.Label(root, text="Arrival Date (YYYY-MM-DD):")
arrival_date_label.grid(row=3, column=0, padx=10, pady=10)

arrival_date_entry = tk.Entry(root)
arrival_date_entry.grid(row=3, column=1, padx=10, pady=10)
arrival_date_entry.insert(0, "2024-07-31")  # Example date

scrape_button = tk.Button(root, text="Scrape & Save", command=scrape_and_save)
scrape_button.grid(row=4, columnspan=2, padx=10, pady=10)

scraped_data_text = tk.Text(root, height=10, width=60)
scraped_data_text.grid(row=5, columnspan=2, padx=10, pady=10)

# Start the scheduling function in a separate thread
schedule_scraping_thread = threading.Thread(target=schedule_scraping)
schedule_scraping_thread.start()

root.mainloop()
