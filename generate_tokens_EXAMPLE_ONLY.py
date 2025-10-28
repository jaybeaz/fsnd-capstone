import requests
import json

AUTH0_DOMAIN = 'dev-2chb8bw0zdh1z1um.us.auth0.com'
API_AUDIENCE = 'fsnd-casting-agency-capstone'
CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # for demo purposes only
CLIENT_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # for demo purposes only

def get_token(username, password):
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    headers = {'content-type': 'application/json'}
    body = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'audience': API_AUDIENCE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'openid profile email',
        'realm': 'Username-Password-Authentication'
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()

# Get tokens for each user
print("=== Casting Assistant Token ===")
assistant = get_token('assistant@test.com', '**************')
print(json.dumps(assistant, indent=2))

print("\n=== Casting Director Token ===")
director = get_token('director@test.com', '**************')
print(json.dumps(director, indent=2))

print("\n=== Executive Producer Token ===")
producer = get_token('executive@test.com', '**************')
print(json.dumps(producer, indent=2))