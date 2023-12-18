import requests
import os

# Authentication
user_id = os.environ.get('DEV_USER_IDENTIFIER')
user_secret = os.environ.get('DEV_USER_SECRET')

auth_url = 'https://api.smartling.com/auth-api/v2/authenticate'
auth_params = {'userIdentifier': user_id, 'userSecret': user_secret}
auth_response = requests.post(auth_url, json=auth_params)

if auth_response.status_code != 200:
    print("Authentication failed:", auth_response.json())
    exit()

access_token = auth_response.json()['response']['data']['accessToken']

# Check Translation Status
project_id = '88ac3c227'  # Your project ID
job_uid = 'bmpqfi5ol7jv'  # Your job UID

status_url = f'https://api.smartling.com/jobs-api/v3/projects/{project_id}/jobs/{job_uid}/progress'
status_headers = {'Authorization': f'Bearer {access_token}'}
status_response = requests.get(status_url, headers=status_headers)

if status_response.status_code == 200:
    progress = status_response.json()['response']['data']['progress']
    if progress is not None:
        print('Job Progress:', str(progress['percentComplete']) + '% complete.')
    else:
        print('Job Progress: 0% complete!')
else:
    print(status_response.status_code)
    print(status_response.text)
