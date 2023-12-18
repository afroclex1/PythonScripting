import os
import requests
import json

# Read authentication credentials from environment
user_id = os.environ.get('DEV_USER_IDENTIFIER')
user_secret = os.environ.get('DEV_USER_SECRET')
project_id = os.environ.get('DEV_PROJECT_ID')

# Print out the environment variables to verify
print("User ID:", user_id)
print("User Secret:", user_secret)
print("Project ID:", project_id)

# Authenticate
api_url = 'https://api.smartling.com/auth-api/v2/authenticate'
api_parameters = {
    'userIdentifier': user_id,
    'userSecret': user_secret
}
api_response = requests.post(api_url, json=api_parameters)

# Check if authentication was successful
if api_response.status_code == 200 and 'accessToken' in api_response.json()['response']['data']:
    # Store access token for use in subsequent API calls
    access_token = api_response.json()['response']['data']['accessToken']
    print("Authentication successful. Access token:", access_token)
else:
    print("Authentication failed. Response:", api_response.json())
