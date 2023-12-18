import requests
import json
import os

# Authenticate
user_id = os.environ.get('DEV_USER_IDENTIFIER')
user_secret = os.environ.get('DEV_USER_SECRET')

api_url = 'https://api.smartling.com/auth-api/v2/authenticate'
api_parameters = {
    'userIdentifier': user_id,
    'userSecret': user_secret
}
auth_response = requests.post(api_url, json=api_parameters)

if auth_response.status_code == 200:
    access_token = auth_response.json()['response']['data']['accessToken']
    print("Authentication successful. Access token:", access_token)

    # Create Translation Job
    project_id = os.environ.get('DEV_PROJECT_ID')
    job_name = 'Test Job 1'
    api_url = f'https://api.smartling.com/jobs-api/v3/projects/{project_id}/jobs'
    api_request_headers = {'Authorization': f'Bearer {access_token}'}
    api_parameters = {
        'jobName': job_name
    }
    job_response = requests.post(api_url, headers=api_request_headers, json=api_parameters)

    if job_response.status_code == 200:
        job_uid = job_response.json()['response']['data']['translationJobUid']
        print('Job UID =', job_uid)
    else:
        print('Failed to create job. Status code:', job_response.status_code)
        print('Response:', job_response.text)
else:
    print('Authentication failed. Status code:', auth_response.status_code)
    print('Response:', auth_response.json())
