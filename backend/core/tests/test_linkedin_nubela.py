import requests

api_key = 'rAzXkl2CyJUErMS8EF58Sg'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
    'linkedin_profile_url': 'https://linkedin.com/in/andrewyng/',
    'fallback_to_cache': 'on-error',
    'use_cache': 'if-present',
    'skills': 'include',
    'inferred_salary': 'include',
    'personal_email': 'include',
    'personal_contact_number': 'include',
    'twitter_profile_id': 'include',
    'facebook_profile_id': 'include',
    'github_profile_id': 'include',
    'extra': 'include',
}
# response = requests.get(api_endpoint,
#                         params=params,
#                         headers=headers)

with open ("/root/hongyu/customersupportgpt/quivr_project/backend/core/tests/test_files/test_linkedin_proxycurl.txt", 'r') as f:
    response_text = f.read()
# print(response.text)

# import json
# res_dict = json.loads(response_text)
# print(res_dict)