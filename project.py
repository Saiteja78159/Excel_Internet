import requests
from bs4 import BeautifulSoup
import json
import os

# URL of the career page
url = "https://www.excel-internet.com/career"

# Directory where you want to save the JSON file
output_folder = "job_json_data"

# Ensure the directory exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Send a GET request to fetch the page content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # List to store job details
    job_list = []

    # Find all job divs with class 'panel panel-default panel-faq'
    job_panels = soup.find_all('div', class_='panel panel-default panel-faq')

    # Iterate over each panel to extract job details
    for panel in job_panels:
        # Extract the job title
        job_title = panel.find('h4', class_='panel-title').text.strip()

        # Extract the location (inside the panel-body)
        location = panel.find('h4', class_='page-header').text.split('Location:')[1].split('<')[0].strip()

        # Extract the job description (the paragraphs inside panel-body)
        job_description = panel.find('div', class_='panel-body').find_all('p')[1].text.strip()

        # Extract eligibility criteria (WHO YOU ARE section)
        eligibility_criteria = panel.find_all('p')[3].text.strip()

        # Extract years of experience safely (check if list has enough elements)
        years_of_exp = "Not specified"
        list_items = panel.find_all('li')
        for li in list_items:
            if "Minimum" in li.text:
                years_of_exp = li.text.strip()
                break  # Stop once we find the right li

        # Store the job details in a dictionary
        job_data = {
            'company': 'ITC Infotech',
            'job_title': job_title,
            'eligibility_criteria': eligibility_criteria,
            'job_description': job_description,
            'years_of_exp': years_of_exp,
            'location': location,
            'job_type': 'Full-time'  # Assuming full-time, modify if dynamic
        }
        job_list.append(job_data)

    # Define the path where the JSON file will be saved
    output_path = os.path.join(output_folder, 'jobs.json')

    # Save the job list to the JSON file inside the specified folder
    with open(output_path, 'w') as file:
        json.dump(job_list, file, indent=4)

    print(f"Job details saved to {output_path}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
