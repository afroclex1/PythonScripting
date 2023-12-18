import requests
import os

# Authentication
user_id = os.environ.get('DEV_USER_IDENTIFIER')
user_secret = os.environ.get('DEV_USER_SECRET')
project_id = os.environ.get('DEV_PROJECT_ID')

auth_url = 'https://api.smartling.com/auth-api/v2/authenticate'
auth_params = {'userIdentifier': user_id, 'userSecret': user_secret}
auth_response = requests.post(auth_url, json=auth_params)

if auth_response.status_code != 200:
    print("Authentication failed:", auth_response.json())
    exit()

access_token = auth_response.json()['response']['data']['accessToken']

# Create Translation Job
job_name = 'Test Job 1'
job_url = f'https://api.smartling.com/jobs-api/v3/projects/{project_id}/jobs'
job_headers = {'Authorization': f'Bearer {access_token}'}
job_params = {'jobName': job_name}
job_response = requests.post(job_url, headers=job_headers, json=job_params)

if job_response.status_code != 200:
    print("Failed to create job:", job_response.json())
    exit()

job_uid = job_response.json()['response']['data']['translationJobUid']

# Create Job Batch
file_uris = [job_uid + '/test-files/site-navigation.json', job_uid + '/test-files/products.json']
batch_url = f'https://api.smartling.com/job-batches-api/v2/projects/{project_id}/batches'
batch_params = {'authorize': False, 'translationJobUid': job_uid, 'fileUris': file_uris}
batch_response = requests.post(batch_url, headers=job_headers, json=batch_params)

if batch_response.status_code != 200:
    print("Failed to create batch:", batch_response.json())
    exit()

batch_uid = batch_response.json()['response']['data']['batchUid']

# Upload Files to the Batch
FILE_LIST = [
    'test-files/site-navigation.json',
    'test-files/products.json'
]
LOCALE_LIST = ['fr-FR']  # Adjust as needed

upload_url = f'https://api.smartling.com/job-batches-api/v2/projects/{project_id}/batches/{batch_uid}/file'
for file_name in FILE_LIST:
    file_path = f'C:\\Users\\Alex Caffrey\\PycharmProjects\\SmartlingAPI\\Test 2\\{file_name}'
    file_uri = job_uid + '/' + file_name
    upload_params = {
        'fileUri': file_uri,
        'fileType': 'json',
        'localeIdsToAuthorize[]': LOCALE_LIST
    }
    with open(file_path, 'rb') as file_data:
        upload_response = requests.post(upload_url, headers=job_headers, data=upload_params, files={'file': file_data})
        if upload_response.status_code == 202:
            print('Uploaded file', file_name)
        else:
            print('Failed to upload file:', file_name)
            print(upload_response.status_code)
            print(upload_response.text)
