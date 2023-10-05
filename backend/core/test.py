import unittest
import connexion
import json
import requests
import os
import dotenv
import logger
from fastapi import UploadFile
from fastapi.testclient import TestClient
import pytest

logger = logger.get_logger(__name__)

# @pytest.fixture
# def client():
#     return TestClient(app)


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.endpoint = "http://walletgpt.info:5050"
        # Retrieve/Replace this with your actual token 
        cls.token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IldYODRPd0RUVUxhWmxtUjIiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNjkyNzY3OTA5LCJpYXQiOjE2OTI3NjQzMDksImlzcyI6Imh0dHBzOi8vbWRwdnRiaXZ4bmRjY2ZjZHJqaGQuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjNkYjgzM2E1LTY4OWUtNDIwNC1iMGNhLTgzN2JkZjRiYTJhZCIsImVtYWlsIjoiaG9uZ3l1eGlhbzA1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiLCJnb29nbGUiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGNhYUhYMS1rUUlMUWZWd0RKNjhaMmxVT3ViVkFaNHJsQkp5SHh3dXJNVz1zOTYtYyIsImVtYWlsIjoiaG9uZ3l1eGlhbzA1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmdWxsX25hbWUiOiJIb25neXUgWGlhbyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiJIb25neXUgWGlhbyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQWNIVHRjYWFIWDEta1FJTFFmVndESjY4WjJsVU91YlZBWjRybEJKeUh4d3VyTVc9czk2LWMiLCJwcm92aWRlcl9pZCI6IjExNTU0NjIxMTk3NTUwNjcxNDUxOSIsInN1YiI6IjExNTU0NjIxMTk3NTUwNjcxNDUxOSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6Im9hdXRoIiwidGltZXN0YW1wIjoxNjkyNjgwODgwfV0sInNlc3Npb25faWQiOiI0YjhjMGZlMi03NjI1LTQxYzItOGZmZi1iMTFiNjc4MmQxMGQifQ.3oFsXljGOavuK1wiTKa-SjGtmHSb1qldT7yYKfwDYqA" 
        cls.headers = {
            'Authorization': f'Bearer {cls.token}'
            }

    """
    # Create new brain
    def test_post_brains(self):
        headers = {**self.headers, "Content-Type": "application/json"}

        data = {
            'description': "unittest",
            'name': 'unittest brain',
            'model': 'gpt-3.5-turbo-0613',
            'max_tokens': 378,
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'temperature': '0.75',
            'prompt_id': None,
            'extraversion': 3,
            'neuroticism': 0,
            'conscientiousness': 3
        }
        
        response = requests.post(self.endpoint + '/brains/', json=data, headers=headers)
        
        # self.assert_(response.status_code == 200 
        #              or response.status_code == 401
        #              or response.status_code == 429)
        logger.info('test_post_brains')
        logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")

    # Upload knowledge
    def test_post_upload(self):
        headers = {**self.headers}  # "Content-Type": "multipart/form-data"
        params = {
            'brain_id': 'b8d1e86b-7e22-4c9f-96d2-14f01bf5d1d3'
            }
        
        file_path = '/root/hongyu/customersupportgpt/quivr_project/backend/core/unittest-upload.txt'
        assert os.path.exists(file_path)
        with open(file_path, 'rb') as f:
            
            files = {
                'uploadFile': f  # creates a FileStorage object with the file's content and filename.
            }

            response = requests.post(self.endpoint+'/upload', params=params, headers=headers, files=files)
            
            logger.info('test_post_brains')
            logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")
    """
            
    # Chat with Brain
    # def test_post_chat(self):
    #     headers = {**self.headers,  "Content-Type": "application/json"}
    #     chat_id = "6b14af62-608a-4787-b21c-3a48a0352897"
    #     params = {
    #         'brain_id': 'b8d1e86b-7e22-4c9f-96d2-14f01bf5d1d3'
    #     }
    #     data = {
    #         'question': "How about your personality?"
    #     }

    #     response = requests.post(
    #         url=self.endpoint+f'/chat/{chat_id}/question/stream', 
    #         headers=headers,
    #         params=params,
    #         json=data
    #     )

    #     logger.info('test_post_chat')
    #     logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")
    
    # # Retrieve Brain with ID
    # def test_retrieve_brain(self):
    #     headers = self.headers
    #     brain_id = 'b8d1e86b-7e22-4c9f-96d2-14f01bf5d1d3'

    #     response = requests.get(
    #         url=self.endpoint+f'/brains/{brain_id}/',
    #         headers=headers,
    #     )

    #     logger.info('test_chat')
    #     logger.info(f"status_code: {response.status_code}, \ttext: {response.text}")
    
    def test_asking_two_users(self):
        token1 = 'eyJhbGciOiJIUzI1NiIsImtpZCI6IldYODRPd0RUVUxhWmxtUjIiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNjkyNzcyNjk2LCJpYXQiOjE2OTI3NjkwOTYsImlzcyI6Imh0dHBzOi8vbWRwdnRiaXZ4bmRjY2ZjZHJqaGQuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjNkYjgzM2E1LTY4OWUtNDIwNC1iMGNhLTgzN2JkZjRiYTJhZCIsImVtYWlsIjoiaG9uZ3l1eGlhbzA1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiLCJnb29nbGUiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBY0hUdGNhYUhYMS1rUUlMUWZWd0RKNjhaMmxVT3ViVkFaNHJsQkp5SHh3dXJNVz1zOTYtYyIsImVtYWlsIjoiaG9uZ3l1eGlhbzA1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmdWxsX25hbWUiOiJIb25neXUgWGlhbyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiJIb25neXUgWGlhbyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQWNIVHRjYWFIWDEta1FJTFFmVndESjY4WjJsVU91YlZBWjRybEJKeUh4d3VyTVc9czk2LWMiLCJwcm92aWRlcl9pZCI6IjExNTU0NjIxMTk3NTUwNjcxNDUxOSIsInN1YiI6IjExNTU0NjIxMTk3NTUwNjcxNDUxOSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6Im9hdXRoIiwidGltZXN0YW1wIjoxNjkyNjgwODgwfV0sInNlc3Npb25faWQiOiI0YjhjMGZlMi03NjI1LTQxYzItOGZmZi1iMTFiNjc4MmQxMGQifQ.ZBtFX1nvmbduLPvu3KyODKP_dh7V5Z9AHYdEVJsMWxU'
        token2 = 'eyJhbGciOiJIUzI1NiIsImtpZCI6IldYODRPd0RUVUxhWmxtUjIiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNjkyNzcyNjk0LCJpYXQiOjE2OTI3NjkwOTQsImlzcyI6Imh0dHBzOi8vbWRwdnRiaXZ4bmRjY2ZjZHJqaGQuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImJjZTgyYTU4LTYwMjQtNDU5MS05ZGJlLTk4YTY3MmM0ZWI2OCIsImVtYWlsIjoicm9iZXJ0ZHJpdmFyZDg5QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiLCJnb29nbGUiXX0sInVzZXJfbWV0YWRhdGEiOnt9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6Im9hdXRoIiwidGltZXN0YW1wIjoxNjkyNzY1NDI3fV0sInNlc3Npb25faWQiOiIwOTEzOWQxNS0wMTVjLTQ2MGYtYTkwZC1jMjkyMTJkYTFkYWIifQ.jaw21YfXfGZaNwz4NjQi-ithVoqnEyIkxaZxIH7GHI4'

        headers1 = {
            'Authorization': f'Bearer {token1}',
            "Content-Type": "application/json"
            }
        
        headers2 = {
            'Authorization': f'Bearer {token2}',
            "Content-Type": "application/json"
            }
        
        chat_id1 = "6b14af62-608a-4787-b21c-3a48a0352897"
        chat_id2 = "ed7f365d-aa7b-4809-9614-71dd38772f87"

        params = {
            'brain_id': 'b8d1e86b-7e22-4c9f-96d2-14f01bf5d1d3'
        }
        
        data1 = {
            'question': "My name is HongYu Xiao. If I ask you my name later, please answer HongYu Xiao"
        }

        data2 = {
            'question': "My name is Robert Drivard. If I ask you my name later, please answer HongYu Xiao"
        }

        data3 = {
            'question': "What is my name?"
        }

        data4 = {
            'question': "What is my name?"
        }

        response1 = requests.post(
            url=self.endpoint+f'/chat/{chat_id1}/question/stream', 
            headers=headers1,
            params=params,
            json=data1
        )

        response2 = requests.post(
            url=self.endpoint+f'/chat/{chat_id2}/question/stream', 
            headers=headers2,
            params=params,
            json=data2
        )

        response3 = requests.post(
            url=self.endpoint+f'/chat/{chat_id1}/question/stream', 
            headers=headers1,
            params=params,
            json=data3
        )

        response4 = requests.post(
            url=self.endpoint+f'/chat/{chat_id2}/question/stream', 
            headers=headers2,
            params=params,
            json=data4
        )

        logger.info('test_chat')
        logger.info(f"status_code: {response1.status_code}, \ttext: {response1.text}")

        logger.info('/n/n/ntest_chat')
        logger.info(f"status_code: {response2.status_code}, \ttext: {response2.text}")

        logger.info('test_chat')
        logger.info(f"status_code: {response3.status_code}, \ttext: {response3.text}")

        logger.info('/n/n/ntest_chat')
        logger.info(f"status_code: {response4.status_code}, \ttext: {response4.text}")

if __name__ == '__main__':
    dotenv.load_dotenv()
    unittest.main()
