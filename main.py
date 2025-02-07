import time 
import csv
import requests
import json

# request API
api_url = "https://pultegroup.wd1.myworkdayjobs.com/wday/cxs/pultegroup/PGI/jobs"

# request headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Referer": "https://pultegroup.wd1.myworkdayjobs.com/en-US/PGI",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

# body payload
payload = {
    "appliedFacets": {},
    "limit": 20,  # default 20 in the dev tool
    "offset": 0,  # default 0 in the dev tool
    "searchText": ""
}

# store all jobs
all_jobs = []
offset = 0
limit = 20
page = 1
job_counter = 0

while True:
    payload['offset'] = offset
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print("Failed to load page")
        break

    data = response.json()
    #Eafter offset 0, the total number is always 0 on the website, so just collect it at the beginning.
    if offset == 0:
        job_number = data.get("total", 0)
    
    
    jobs = data.get("jobPostings", [])

    if not jobs:
        print("No more job postings found.")
        break

    for job in jobs:
        job_title = job.get('title', '')
        job_location = job.get('locationsText', '')
        job_posting_date = job.get('postedOn', '')
        job_id = job.get('bulletFields', '')[0]
        job_link = job.get('externalPath', '')
        all_jobs.append([job_title, job_location, job_posting_date, job_id, job_link])
        job_counter += 1
        # print(f"Job {job_counter}: {job_title}")

    if job_counter >= job_number:
        break

    offset += limit
    page += 1
    time.sleep(3)

with open ('jobs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Job Location', 'Job Posting Date', 'Job ID', 'Job Link'])
    writer.writerows(all_jobs)
    print(f"Total {job_counter} jobs saved to jobs.csv")
