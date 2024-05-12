# FlyFetch

## Video Demonstration


https://github.com/musman12529/Flights-Scrapper/assets/114633620/a869b47f-6eed-4393-950d-e045e8b53ec2



## Overview
FlyFetch is a Python application designed to scrape flight data from Kayak using Selenium and BeautifulSoup. It allows users to specify the departure location, destination, departure date, and arrival date to retrieve flight information. The scraped data is saved to a CSV file and also sent via email.

## Features
- **Scraping Functionality**: Scrapes flight data from Kayak based on user input.
- **GUI Interface**: Provides a user-friendly graphical interface using Tkinter for input and display of scraped data.
- **Robots.txt Compliance**: Checks whether scraping is allowed based on the robots.txt file of the website.
- **CSV Export**: Saves the scraped flight data to a CSV file with a timestamp.
- **Email Notification**: Sends an email containing the scraped flight data to the specified email address.
- **Scheduled Scraping**: Automatically scrapes flight data at regular intervals using the schedule library.
- **Threading**: Runs the scheduling function in a separate thread to avoid blocking the GUI.

## Requirements
- Python 3.x
- Tkinter
- BeautifulSoup
- Selenium
- Pandas
- Schedule
- smtplib

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/flight-scraper.git
    cd flight-scraper
    ```
2. Install the required dependencies:
    

## Usage
1. Run the `flight_scraper.py` file:
    ```bash
    python flight_scraper.py
    ```
2. Enter the departure location, destination, departure date, and arrival date in the provided fields.
3. Click on the "Scrape & Save" button to initiate scraping.
4. The scraped flight data will be displayed in the text area and saved to a CSV file.
5. Check your email for the flight data notification.

## Note
- Ensure that you have a compatible version of the Chrome WebDriver installed and its path set correctly. You can download it from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
- Update the email credentials in the `email_sender` function with valid Gmail credentials.
- Make sure to review the terms of use and scraping policies of Kayak before using this tool for commercial purposes.


