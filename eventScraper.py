

cookies = {'production_submitted_email_address': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IkltdDJhV0oxYUhReFFIVnRZbU11WldSMUlnPT0iLCJleHAiOiIyMDQ0LTA5LTIzVDE0OjQ4OjUzLjc0OVoiLCJwdXIiOm51bGx9fQ%3D%3D--19d4143e73cd7b7739aa394589e261d040b83ad8',
    'production_current_user': '46795941',
    'hss-global': 'eyJhbGciOiJkaXIiLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwidHlwIjoiSldUIn0..317usG6DXkBrqfTcwGTqAw.FxGXuAsLJ05J_LqT2btNLFL3YgFPtGZLkPFKiOTbmbBhStxZEMBV3aU81Ud-cvgtFvddTyEN-Cq6n_PXEs2wtbqwgW66mUMUpR7iP8WheYCq3ke-trVGnoIjN0aM8XYmewgPAQemY1IrQdoO6s37bBvaLzeM6kmcUmAfPztPf4a1XTXq90oZQ9QfsEmLYK11YqJTsdQGikg5t351kMrK-3Rtf7x3JCDq3_UOz7_j7w6ZtqiQCBPDMEG8G2qB9zOGQXJLlufjBA4m2CfYTOsr2WBaPiU8YUR1d54f7p___yAIJJIKtnaFd3OUFGX7i9rKSU6OM_OWQxGaJsB0rWDe1IC910yZcQL9LR1Ua4p9CXPWPF48NRquS1jW52HCKJc3.Ws5VO6FgEnLu-Rf0Qs5k5R7CYKsxT6vDRM6Z7-_o7Q8',
    '_trajectory_session': 'lvpZ%2Bx6e1xuxsUbMvzhgwQSlmtqXdmR%2F1MIkvGX0JfUEHg9dcU0cDTPsaAKCjj60vFzkXdpakQEuugbz9fuGMQxsrK4mdk4JuCJ55h5cAjOKpGlBeEZA%2BfNnJEupzse0UtB%2BSMiQSsEXhhTj0pqvmCMs1mGh2MBl7fLcaHwsU64sphhKgtl0XLWv07Im%2BxHk1aRQd01vYbIMcYlmoiBFOgZaSbHrLnDhlgOrLe76ZTB%2FMMzlEazdrOQqHrCLtNEr3B%2BiGg1PSMhmZG2nAj0fNUuLVUtTtZh3YwNTxnon9M960xyp0pyyomlxKPegqLU7WfJfsk%2FCIJuJvA%3D%3D--YF44eRLq8h20ZUCZ--%2BCBEINlgwzT0jfQpFfdSog%3D%3D',
    'production_js_on': 'true',
    'production_46795941_incident-warning-banner-show': '%5B%5D',}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #'Referer': 'https://app.joinhandshake.com/stu/events',
    'X-CSRF-Token': 'OMKrob0EBU1MO69XigLI9JH6Ykn8kVZgYF+TNXyE/FPoUyASCFdY1bbQbRK/seUQZ305Ks+mAv8CjHFFfom7Ew==',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
import json
import csv
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")  # Disable sandboxing for headless
options.add_argument("--disable-dev-shm-usage")  # Fixes issues with shared memory

# Uncomment for headless if needed
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = ChromeService(ChromeDriverManager(driver_version="131.0.6778.85").install())
driver = webdriver.Chrome(options=options, service=service)
# Set the script timeout to a higher value (e.g., 60 seconds)

URL = "https://app.joinhandshake.com"
# Navigate to the main Handshake URL (to inject cookies properly)
driver.get(URL)

# Wait for the page to load before injecting cookies
time.sleep(5)  # Adjust this if necessary depending on page load time



# Inject cookies into the browser
for name, value in cookies.items():
    cookie_dict = {
        'name': name,
        'value': value,
        'domain': 'app.joinhandshake.com',
        'path': '/',
    }
    driver.add_cookie(cookie_dict)

# Refresh the page to log in with cookies
driver.refresh()
driver.set_script_timeout(60)
# At this point, the browser should be logged in, and you can continue scraping
# Now proceed with your scraping logic
driver.get("https://app.joinhandshake.com/stu/events")

# Your scrolling logic here
def scroll_to_bottom(driver, pause_time=15):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the page to load more content
        time.sleep(pause_time)
        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll down to the bottom of the page to load all events
scroll_to_bottom(driver)

# Get the full page source after all events are loaded
page_source = driver.page_source

# Close the driver as we no longer need it
driver.quit()



def fetch_data(url, params=None, cookies=None, headers=None):
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return None
    
def get_event_description(event_id, cookies=None, headers=None):
    event_url = f"https://app.joinhandshake.com/stu/events/{event_id}"
    print(f"Fetching description for event: {event_id}")  # Debugging info

    try:
        content = fetch_data(event_url, cookies=cookies, headers=headers)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            #print(soup)
            try:
                site_json = json.loads(soup.text)  # Parse JSON data
                event_info = {
                    'Type': site_json['event'].get('type', 'N/A'),
                    'id': site_json['event'].get('id', 'N/A'),
                    'Name': site_json['event'].get('name', 'N/A'),
                    'Start Date': site_json['event'].get('start_date', 'N/A'),
                    'End Date': site_json['event'].get('end_date', 'N/A'),
                    'Host Name': site_json['event'].get('host_name', 'N/A'),
                    'Event URL': site_json['event'].get('external_link', 'N/A'),
                    'description': site_json['event'].get('description', 'N/A')
                }
                return event_info
            except json.JSONDecodeError:
                print(f"Failed to parse JSON from {event_url}")
                return {"Error": "Failed to retrieve description"}
        else:
            print(f"No content returned for {event_url}")
            return {"Error": "Failed to retrieve description"}
    except Exception as e:
        print(f"Error fetching event description from {event_url}: {str(e)}")
        return {"Error": "Failed to retrieve description"}

    
def parse_data(content):
    soup = BeautifulSoup(content, 'html.parser')
    anchors = soup.find_all('a', href=True)
    event_ids = []
    for anchor in anchors:
        href = anchor['href']
        # Check if href matches the desired pattern (starts with "/stu/events/")
        if href.startswith('/stu/events/'):
            # Split the href by '/' and '?' to extract the ID
            event_id = href.split('/stu/events/')[1].split('?')[0]
            event_ids.append(event_id)
    #print(event_ids)
    events_data = []
    for event in event_ids:
        
        event_info = get_event_description(event, cookies, headers)
        events_data.append(event_info)

    return events_data

def write_to_csv(data, filename="events_list.csv"):
    fieldnames = ["Type","id", "Name", "Start Date", "End Date", "Host Name", "Event URL","description"]
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for event in data:
            writer.writerow(event)
    print(f"{filename} created successfully!")
    
    print(f"Data written to {filename}")

def scrape_event_data(page, cookies=None, headers=None, params=None, output_file="events_list.csv"):
    if page:
        events = parse_data(page)
        events
        write_to_csv(events, output_file)
        #return content

import pandas as pd

from bs4 import BeautifulSoup
   
import logging
import sys
import pandas as pd


def clean_html(text):
    """
    Removes HTML tags from the input text.
    
    Args:
    - text: A string with HTML content.
    
    Returns:
    - A cleaned string without HTML tags.
    """
    return BeautifulSoup(text, "html.parser").get_text()

# Setup logging in append mode with a specific file for event scraping
logging.basicConfig(
    filename='/home/ubuntu/finalproject/logs/scraping.log',  # Specific log file for event scraping
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Ensure logging happens in append mode
)

logging.info("Starting scraping for events...")
try:
    # Call scraping functions here
    scrape_event_data(page_source)  # Ensure that this function is defined elsewhere
    df = pd.read_csv("events_list.csv")
    df["description"] = df["description"].apply(clean_html)  # Ensure that the clean_html function is defined elsewhere
    df.rename(columns={
        'Type': 'event_type',
        'id': 'event_id',
        'Name': 'name',
        'Start Date': 'start_date',
        'End Date': 'end_date',
        'Host Name': 'host_name',
        'Event URL': 'event_url',
        'description': 'description'
    }, inplace=True)
    df.to_csv("events_list_latest_new.csv")
    logging.info("Event scraping completed successfully.")
except Exception as e:
    logging.error(f"Error during event scraping: {e}")
    sys.exit(1)





