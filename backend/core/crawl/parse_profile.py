import json

def parse_profile(data:dict):
    json_string = json.dumps(data, indent=4)
    return json_string

if __name__ == '__main__':
    with open('/root/hongyu/customersupportgpt/quivr_project/backend/core/tests/test_files/test_linkedin_proxycurl.json', 'r') as file:
        data = json.load(file)
    
    parsed_text = parse_profile(data)
    print(parsed_text)