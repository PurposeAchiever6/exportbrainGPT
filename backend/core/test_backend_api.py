import os
import logger
import requests
from dotenv import load_dotenv


load_dotenv()
logger = logger.get_logger(__name__)

ENDPOINT = "http://walletgpt.info:5050"
# Retrieve/Replace this with your actual token 
TOKEN = "7067d4393182f1a06e3d6628cd492168" 
HEADERS = {
    'Authorization': f'Bearer {TOKEN}'
    }

# Create new brain
def test_post_brains(token, create_brain_data):
    headers = {'Authorization': f'Bearer {token}', "Content-Type": "application/json"}
    response = requests.post(ENDPOINT + '/brains/', json=create_brain_data, headers=headers)

    logger.info('test_post_brains')
    logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")

# Upload knowledge
def test_post_upload(token, brain_id, file_path):
    headers = {'Authorization': f'Bearer {token}'}  # "Content-Type": "multipart/form-data"
    params = {'brain_id': brain_id}
    
    assert os.path.exists(file_path)
    with open(file_path, 'rb') as f:
        files = {
            'uploadFile': f  # creates a FileStorage object with the file's content and filename.
        }
        response = requests.post(ENDPOINT+'/upload', params=params, headers=headers, files=files)
        
        logger.info('test_post_brains')
        logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")

# Chat with Brain
def test_post_chat(token, chat_id, brain_id, question):
    headers = {'Authorization': f'Bearer {token}',  "Content-Type": "application/json"}
    params = {'brain_id': brain_id}
    data = {'question': question}

    response = requests.post(
        url=ENDPOINT+f'/chat/{chat_id}/question/stream', 
        headers=headers,
        params=params,
        json=data
    )

    logger.info('test_post_chat')
    logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")

# Retrieve Brain with ID
def test_retrieve_brain(token, brain_id):
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(
        url=ENDPOINT+f'/brains/{brain_id}/',
        headers=headers,
    )

    logger.info('test_chat')
    logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")

#LinkedIn 
def test_linkedin_scraping(token, brain_id):
    headers = {'Authorization': f'Bearer {token}'}
    params = {'brain_id': brain_id}
    response = requests.post(ENDPOINT+'/crawl/linkedin', params=params, headers=headers)

    logger.info('test_linkedin_scraping')
    logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")


if __name__ == "__main__":
    create_brain_data = {
        'description': "unittest",
        'name': 'unittest brain',
        'model': 'gpt-3.5-turbo-0613',
        'max_tokens': 378,
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'temperature': '0.75',
        'prompt_id': None,
        'linkedin': None,
        'extraversion': 3,
        'neuroticism': 0,
        'conscientiousness': 3
    }

    brain_id = 'b8d1e86b-7e22-4c9f-96d2-14f01bf5d1d3'
    file_path = '/root/hongyu/customersupportgpt/quivr_project/backend/core/unittest-upload.txt'
    chat_id = "6b14af62-608a-4787-b21c-3a48a0352897"
    question = "How about your personality?"

    hongyu_token = "7067d4393182f1a06e3d6628cd492168"

    ## Create experts
    andrew_data = {
        'name': 'Andrew NG',
        'description': "Andrew NG, cofounder of Coursera, AI Expert",
        'model': 'gpt-3.5-turbo-0613',
        'max_tokens': 256,
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'temperature': '0.5',
        'prompt_id': None,
        'linkedin': "https://www.linkedin.com/in/andrewyng",
        'extraversion': 2,
        'neuroticism': 1,
        'conscientiousness': 3
    }

    jeffBezos_data = {
        'name': 'Jeff Bezos',
        'description': "Jeff Bezos, businessman and founder of Amazon.com",
        'model': 'gpt-3.5-turbo-0613',
        'max_tokens': 256,
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'temperature': '0.3',
        'prompt_id': None,
        'linkedin': "https://www.linkedin.com/pulse/jeff-bezos-md-yasin-islam",
        'extraversion': 1,
        'neuroticism': 2,
        'conscientiousness': 2
    }

    # test_post_brains(hongyu_token, andrew_data)
    # test_post_brains(hongyu_token, jeffBezos_data)

    andrew_brain_id = "7b78d424-4d17-4ef1-bcea-f28de168c5d9"
    jeff_brain_id = "18c768d5-6096-447a-b5e5-0f8a267bc09a"

    test_linkedin_scraping(token=hongyu_token, brain_id=andrew_brain_id)