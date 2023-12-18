import requests
import os

# Set the Project ID and Locale List
project_id = '88ac3c227'
LOCALE_LIST = ['fr-FR']  # Replace with your locale list

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

# Check Job Progress
job_uid = 'b9gbtysr4jxd'
status_url = f'https://api.smartling.com/jobs-api/v3/projects/{project_id}/jobs/{job_uid}/progress'
status_headers = {'Authorization': f'Bearer {access_token}'}
status_response = requests.get(status_url, headers=status_headers)

if status_response.status_code == 200:
    progress_data = status_response.json()['response']['data']
    if progress_data and 'progress' in progress_data and progress_data['progress']:
        progress = progress_data['progress']
        if progress['percentComplete'] == 100:
            print('Job Progress: 100% complete. Downloading files...')

            # Download Translated Files
            FILE_LIST = [f'output_files/file_{i}.json' for i in range(1, 101)]
            for file_name in FILE_LIST:
                for locale_id in LOCALE_LIST:
                    file_uri = job_uid + '/' + file_name
                    download_url = f'https://api.smartling.com/files-api/v2/projects/{project_id}/locales/{locale_id}/file'
                    download_params = {
                        'fileUri': file_uri,
                        'retrievalType': 'published',
                        'includeOriginalStrings': True
                    }
                    download_response = requests.get(download_url, headers=status_headers, params=download_params)
                    if download_response.status_code == 200:
                        translated_file_name = file_name.replace('output_files/', '').replace('.json', f'_{locale_id}.json')
                        with open(translated_file_name, 'wb') as f:
                            f.write(download_response.content)
                        print('Downloaded', translated_file_name)
                    else:
                        print(download_response.status_code)
                        print(download_response.text)
        else:
            print('Job Progress:', str(progress['percentComplete']) + '% complete. Not ready for download.')
    else:
        print('Progress data not available or job progress not started.')
else:
    print(status_response.status_code)
    print(status_response.text)
