URL = "https://app.joinhandshake.com/stu/postings"

cookies = {'production_submitted_email_address': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IkltdDJhV0oxYUhReFFIVnRZbU11WldSMUlnPT0iLCJleHAiOiIyMDQ0LTA5LTIzVDE0OjQ4OjUzLjc0OVoiLCJwdXIiOm51bGx9fQ%3D%3D--19d4143e73cd7b7739aa394589e261d040b83ad8',
    'production_current_user': '46795941',
    'hss-global': 'eyJhbGciOiJkaXIiLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwidHlwIjoiSldUIn0..317usG6DXkBrqfTcwGTqAw.FxGXuAsLJ05J_LqT2btNLFL3YgFPtGZLkPFKiOTbmbBhStxZEMBV3aU81Ud-cvgtFvddTyEN-Cq6n_PXEs2wtbqwgW66mUMUpR7iP8WheYCq3ke-trVGnoIjN0aM8XYmewgPAQemY1IrQdoO6s37bBvaLzeM6kmcUmAfPztPf4a1XTXq90oZQ9QfsEmLYK11YqJTsdQGikg5t351kMrK-3Rtf7x3JCDq3_UOz7_j7w6ZtqiQCBPDMEG8G2qB9zOGQXJLlufjBA4m2CfYTOsr2WBaPiU8YUR1d54f7p___yAIJJIKtnaFd3OUFGX7i9rKSU6OM_OWQxGaJsB0rWDe1IC910yZcQL9LR1Ua4p9CXPWPF48NRquS1jW52HCKJc3.Ws5VO6FgEnLu-Rf0Qs5k5R7CYKsxT6vDRM6Z7-_o7Q8',
    '_trajectory_session': 'lvpZ%2Bx6e1xuxsUbMvzhgwQSlmtqXdmR%2F1MIkvGX0JfUEHg9dcU0cDTPsaAKCjj60vFzkXdpakQEuugbz9fuGMQxsrK4mdk4JuCJ55h5cAjOKpGlBeEZA%2BfNnJEupzse0UtB%2BSMiQSsEXhhTj0pqvmCMs1mGh2MBl7fLcaHwsU64sphhKgtl0XLWv07Im%2BxHk1aRQd01vYbIMcYlmoiBFOgZaSbHrLnDhlgOrLe76ZTB%2FMMzlEazdrOQqHrCLtNEr3B%2BiGg1PSMhmZG2nAj0fNUuLVUtTtZh3YwNTxnon9M960xyp0pyyomlxKPegqLU7WfJfsk%2FCIJuJvA%3D%3D--YF44eRLq8h20ZUCZ--%2BCBEINlgwzT0jfQpFfdSog%3D%3D',
    'production_js_on': 'true',
    'production_46795941_incident-warning-banner-show': '%5B%5D',}

headers = {'User-Ageant': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    #'X-CSRF-Token': '56GPQhRCjWsPoTz5u5Uk8tWt52r9SuDC3+NlFjhR+KOpgw87IK/LfgH9Ihzrzf5xSw6jS9ksc/iQKXtTO55TNA==',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    }

params = {
    'page': '1',
    'per_page': '25',
    'sort_direction': 'desc',
    'sort_column': 'default',
    'job.job_applicant_preference.willing_to_sponsor_candidate': 'true',
    'job.job_applicant_preference.accepts_opt_cpt_candidates': 'true',
    'job.job_applicant_preference.work_auth_not_required': 'true',
    'job.industries[]': '1034'
}


import requests
import json
import csv
from bs4 import BeautifulSoup
import pandas as pd

# Function to fetch data from a given URL with parameters
def fetch_data(url, params=None, cookies=None, headers=None):
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return None

# Function to parse the response and extract relevant data
def get_job_description(url, cookies, headers):
    # Fetch the description using the individual job URL
    #print(f"Fetching description for: {url}")  # Debugging info
    try:
        content = fetch_data(url, cookies=cookies, headers=headers)
        if content:  # Ensure you have a response
            soup = BeautifulSoup(content, 'html.parser')
            try:
                site_json = json.loads(soup.text)
                #print(site_json.get('job', {}).get('description', "No description available"))
                return site_json.get('job', {}).get('description', "No description available")  # Use safe dict access
            except json.JSONDecodeError:
                print(f"Failed to parse JSON from {url}")
                return "Failed to retrieve description"
        else:
            print(f"No content returned for {url}")
            return "Failed to retrieve description"
    except Exception as e:
        print(f"Error fetching job description from {url}: {str(e)}")
        return "Failed to retrieve description"

# Make sure the description is unique for each job
def parse_data(content):
    soup = BeautifulSoup(content, 'html.parser')
    site_json = json.loads(soup.text)
    job_postings = []
    for result in site_json['results']:
        employer_name = result['job']['employer_name']
        posting_url = f"https://app.joinhandshake.com/jobs/{result['job']['id']}"  # Construct posting URL
        location_state = result['job']['location_states'][0] if result['job']['location_states'] else None
        location_city = result['job']['location_cities'][0] if result['job']['location_cities'] else None
        employment_type = result['job']['employment_type_name']
        job_title = result['job']['title']
        created_at = result['created_at']
        expiration_date = result['expiration_date']
        apply_start = result['apply_start']
        
        # Fetch unique job description for each posting
        description = get_job_description(posting_url, cookies, headers)
        
        job_postings.append({
            'employer_name': employer_name,
            'posting_url': posting_url,
            'location_state': location_state,
            'location_city': location_city,
            'employment_type': employment_type,
            'job_title': job_title,
            'created_at': created_at,
            'expiration_date': expiration_date,
            'apply_start': apply_start,
            'description': description  # Store unique descriptions
        })
    
    return job_postings

    
    
    
def write_to_csv(data, filename="job_listings.csv", append=False):
    fieldnames = ["employer_name", "posting_url", "location_state", "location_city", "employment_type", "job_title", "created_at", "expiration_date", "apply_start","description"]
    
    # Open file in append mode if specified
    mode = 'a' if append else 'w'
    write_header = not append  # Write header only once
    
    with open(filename, mode, newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for job in data:
            writer.writerow(job)
    
    print(f"Data written to {filename}")

def scrape_employer_data(url, cookies, headers, params=None, output_file="job_listings.csv", num_pages=10):
    for page in range(1, num_pages + 1):  # Loop through each page
        print(f"Fetching page {page}...")
        params['page'] = page  # Set the page number dynamically in params
        content = fetch_data(url, params, cookies, headers)
        if content:
            jobs = parse_data(content)
            # Append jobs to the CSV
            write_to_csv(jobs, output_file, append=(page > 1))  # Append to file after the first page

URL = "https://app.joinhandshake.com/stu/postings"


import logging
import sys
import pandas as pd
from bs4 import BeautifulSoup

import logging
import sys

# Set up logging in append mode with a specific file for job scraping
logging.basicConfig(
    filename='/home/ubuntu/finalproject/logs/scraping.log',  # Specific log file for job scraping
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Ensure logging happens in append mode
)

logging.info("Starting scraping for Jobs...")
try:
    # Call scraping functions here
    scrape_employer_data(URL, cookies, headers, params, "job_listings.csv", num_pages=15)
    logging.info("Job scraping completed successfully job_list.csv.")
except Exception as e:
    logging.error(f"Error during Job scraping: {e}")
    sys.exit(1)

import pandas as pd

df = pd.read_csv('job_listings.csv')

section_definitions = {
    "Required_Qualification": {
        "aliases": [
            "Qualifications", "Requirement", "Requirements", 
            "Required Skills", "Experience", "Skills", 
            "Tool-Kit", "Toolkit", "Key Qualifications", 
            "Key Skills", "BASIC QUALIFICATIONS", "Qualifications (Required)", "What you need"
        ]
    },
    "Preferred_Qualification": {
        "aliases": [
            "Preferred Qualifications", "Preferences", 
            "Desired Skills", "Preferred Skills", 
            "Experience", "Good to Haves", 
            "Good to Have Skills","Qualifications (It’s a plus)"
        ]
    },
    "Responsibilities": {
        "aliases": [
            "Responsibilities", "Duties", "Impact", 
            "Key Responsibilities","What you will do"
        ]
    }
}
from bs4 import BeautifulSoup

def clean_html(text):
    """
    Removes HTML tags from the input text.
    
    Args:
    - text: A string with HTML content.
    
    Returns:
    - A cleaned string without HTML tags.
    """
    return BeautifulSoup(text, "html.parser").get_text()

def segregate_by_headers(description_html):
    """
    Segregates the description based on the occurrence of <p><strong>...</strong></p>.
    Each occurrence of this pattern marks the start of a new section.
    The content inside the <strong> tag is the header and the content following
    the header (until the next header or the end of the document) is stored as the section content.
    
    If no sections are found, the function returns the cleaned description under the key "content".
    
    Args:
    - description_html: HTML content of the job description (as a string)

    Returns:
    - A dictionary with headers as keys and the corresponding content as values.
      If no headers are found, the entire description is returned under the key "content".
    """
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(description_html, 'html.parser')

    # Initialize an empty dictionary to store the sections
    sections = {}
    current_header = None  # To store the current header
    current_content = []   # To accumulate the content for the current section

    # Iterate through the HTML tags
    for tag in soup.find_all(['p', 'ul']):
        if tag.name == 'p' and tag.strong:  # Check for <p><strong>...</strong></p>
            # If there's an existing header, save its content before moving to the new section
            if current_header:
                sections[current_header] = " ".join(current_content).strip()
            
            # Set the new header and reset the content accumulator
            current_header = tag.strong.get_text(strip=True)
            current_content = []
        
        # If not a new header, accumulate the content for the current section
        elif current_header:
            current_content.append(tag.get_text(" ", strip=True))
    
    # Save the content for the last section
    if current_header:
        sections[current_header] = " ".join(current_content).strip()

    # If no sections were created, return the entire cleaned description
    if not sections:
        sections["content"] = clean_html(description_html)

    return sections
df["sections"]= df["description"].apply(segregate_by_headers)

unique_headers = set()

    # Iterate over each row in the DataFrame
for sections_dict in df["sections"]:
    if isinstance(sections_dict, dict):
        unique_headers.update(sections_dict.keys())
unique_headers = list(unique_headers)
import re

# List of sample headers for testing
headers = list(unique_headers)

# Patterns based on required and not required tags
patterns = {
    'you_related': r'\byou\b.*\b(?:are|bring|need|have|will|expect|qualifications|skills|knowledge|responsibilities)\b',
    'we_related': r'\bwe\b.*\b(?:value|require|expect|responsibilities|duties|skills|knowledge|background)\b',
    'general_requirements': r'\b(?:about you|role|about job|qualifications|requirements|background|skills|education|experience|knowledge|ideal candidate|job description|preferred|looking for|expectation|responsibilities|toolkit | content)\b'
}

# Classification function
def classify_headers(headers, patterns):
    you_related = []
    we_related = []
    general_requirements = []

    for header in headers:
        # Check patterns in order of specificity
        if re.search(patterns['you_related'], header.lower()):
            you_related.append(header)
        elif re.search(patterns['we_related'], header.lower()):
            we_related.append(header)
        elif re.search(patterns['general_requirements'], header.lower()):
            general_requirements.append(header)

    return you_related, we_related, general_requirements

# Apply classification
you_related_headers, we_related_headers, general_requirements_headers = classify_headers(headers, patterns)

general_requirements_headers.append(you_related_headers)
df['requirements'] = df['sections'].apply(lambda sections: ', '.join(content for key, content in sections.items() if key in general_requirements_headers))
import numpy as np

df['requirements'].replace('', np.nan, inplace=True)
df['description'] = df['description'].apply(clean_html)
df['requirements'] = df['requirements'].fillna(df['description'])
df['location_state'].fillna('Not provided', inplace=True)
df['location_city'].fillna('Not provided', inplace=True)
df['created_at'] = pd.to_datetime(df['created_at'])
df['expiration_date'] = pd.to_datetime(df['expiration_date'])
df['apply_start'] = pd.to_datetime(df['apply_start'])
df.drop(columns=["sections"],inplace=True)
df["id"] = df["posting_url"].apply(lambda x: x.split('/')[-1])
df["company_type"]="Handshake"
df.to_csv("job_listings_latest_skills_new.csv")
print("Job scraping completed successfully job_list_final_skills.csv")