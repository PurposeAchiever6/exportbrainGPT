# Introduction

## Overview

This part outlines the key points and usage instructions for interacting with the API backend. Please follow the guidelines below to use the backend services effectively.

## FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. FastAPI is a class-based API framework that is built on top of Starlette and Pydantic. FastAPI is a great choice for building APIs because it is easy to use, fast, and has a lot of great features.

We decided to choose FastAPI because it is a modern, fast, and easy-to-use API framework. FastAPI is also very well documented and has a lot of great features that make it easy to build APIs. FastAPI is also very well supported by the community and has a lot of great features that make it easy to build APIs.

## Authentication

The API uses API keys for authentication. You can generate an API key by signing in to the frontend application and navigating to the `/config` page. The API key will be required to authenticate your requests to the backend.

When making requests to the backend API, include the following header:

```http
Authorization: Bearer {api_key}
```

Replace `{api_key}` with the generated API key obtained from the frontend


# How to use the API

## Overview

This part outlines the key points and usage instructions for interacting with the API backend. Please follow the guidelines below to use the backend services effectively.

## Usage Instructions

1. Standalone Backend

   - The backend can now be used independently without the frontend application.
   - Users can interact with the API endpoints directly using API testing tools like Postman.

2. Generating API Key

   - To access the backend services, you need to sign in to the frontend application.
   - Once signed in, navigate to the `/user` page to generate a new API key.
   - The API key will be required to authenticate your requests to the backend.

3. Authenticating Requests

   - When making requests to the backend API, include the following header:
     - `Authorization: Bearer {api_key}`
     - Replace `{api_key}` with the generated API key obtained from the frontend.

# Error Handling
## Overview

This part provides information about common error codes, their descriptions, and examples of scenarios where these errors may occur.

| Error Code | Description                                                                 |
| ---------- | --------------------------------------------------------------------------- |
| 401        | Unauthorized: The request lacks valid authentication credentials.           |
| 403        | Forbidden: The requested operation is not allowed.                          |
| 422        | Unprocessable Entity: The request is well-formed but contains invalid data. |
| 500        | Internal Server Error: An unexpected error occurred on the server.          |

## Error Code: 401

**Description**: The request lacks valid authentication credentials or the provided token/api key is invalid.

Example Scenarios:

- Missing or invalid authentication token/api key.
- Expired authentication token.

## Error Code: 403

**Description**: The requested operation is forbidden due to insufficient privileges or credentials missing.

Example Scenarios:

- Attempting to access a resource without proper authorization.
- Insufficient permissions to perform a specific action.

## Error Code: 422

**Description**: The request is well-formed, but contains invalid data or parameters.

Example Scenarios:

- Invalid input data format.
- Required fields are missing or have incorrect values.

## Error Code: 500

**Description**: An unexpected error occurred on the server.

Example Scenarios:

- Internal server error due to a server-side issue.
- Unhandled exceptions or errors during request processing.


# Chat system

## Brain
1. **Create new brain**
   - HTTP method: POST
   - Endpoint: `/brains/`
   - Description: This endpoint create new brain
    ```json
        headers = {
            "Authorization": "Bearer {token}",
            "Content-Type": "application/json",
        }
        requestbody = {
            "description": string,
            "name": string,
            "model": string,
            "max_tokens": int,
            "openai_api_key": string,
            "temperature": string,
            "prompt_id": UUID,
            "extraversion": int,
            "neuroticism": int,
            "conscientiousness": int
        }
    ```
2. **Upload documents to an expert to train him**

   - HTTP method: POST
   - Endpoint: `/upload`
   - Description: This endpoint upload a document for training the brain.
    ```json
        headers = {
            "Authorization": "Bearer {token}",
            "Content-Type": "application/json"
        }
        params = {
            "brain_id": UUID
        }
        files = {
            "uploadFile": binary
        }
    ```
3. **Add URL for brain to train that**

   - HTTP method: POST
   - Endpoint: `/crawl`
   - Description: This endpoint upload a document for training the brain.
    ```json
        headers = {
            "Authorization": "Bearer {token}",
        }
        params = {
            "brain_id": UUID
        }
        requestbody = {
            "depth": integer,
            "js": boolean,
            "max_pages": integer,
            "max_time": integer,
            "url": string
        }
    ```
## Chat
1. **Chat with brain**
   - HTTP method: POST
   - Endpoint: `/chat/{chat_id}/question/stream`
   - Description: Ask a question to brain in specific chat room.
    ```json
        headers = {
            "Authorization": "Bearer {token}",
            "Content-Type": "application/json"
        }
        chat_id = UUID
        params = {
            "brain_id": UUID
        }
        requestbody = {
            "question": string
        }
    ```

2. **Retrieve history of questions for a given expert**
   - HTTP method: GET
   - Endpoint: `/chat/{brain_id}/brain_history`
   - Description: Ask a question to brain in specific chat room.
    ```json
        headers = {
            "Authorization": "Bearer {token}",
            "Content-Type": "application/json"
        }
        brain_id: UUID
    ```

3. **Retrieve all chats for the current user:**

   - HTTP method: GET
   - Endpoint: `/chat`
   - Description: This endpoint retrieves all the chats associated with the current authenticated user. It returns a list of chat objects containing the chat ID and chat name for each chat.

4. **Delete a specific chat by chat ID:**

   - HTTP method: DELETE
   - Endpoint: `/chat/{chat_id}`
   - Description: This endpoint allows deleting a specific chat identified by its chat ID.

5. **Update chat attributes:**

   - HTTP method: PUT
   - Endpoint: `/chat/{chat_id}/metadata`
   - Description: This endpoint is used to update the attributes of a chat, such as the chat name.

6. **Create a new chat with initial chat messages:**

   - HTTP method: POST
   - Endpoint: `/chat`
   - Description: This endpoint creates a new chat with initial chat messages. It expects the chat name in the request payload.

7. **Add a new question to a chat:**

   - HTTP method: POST
   - Endpoint: `/chat/{chat_id}/question`
   - Description: This endpoint allows adding a new question to a chat. It generates an answer for the question using different models based on the provided model type.


8. **Get the chat history:**
   - HTTP method: GET
   - Endpoint: `/chat/{chat_id}/history`
   - Description: This endpoint retrieves the chat history for a specific chat identified by its chat ID.

## Personality
1. **Get personality test questions**
   - HTTP method: GET
   - Endpoint: `/personality/question`
   - Description: This endpoint generate questions for personality test.
    ```json
        headers = {
            "Authorization": "Bearer {token}",
            "Content-Type": "application/json"
        }
        params = {
            "question_number": int
        }
    ```

2. **Get personality from test result**
   - HTTP method: POST
   - Endpoint: `/personality`
   - Description: This endpoint return personality from personality test result.
    ```json
        headers = {
            "Authorization": "Bearer {token}",
            "Content-Type": "application/json"
        }
        requestbody = {
            "result": [string]
        }
    
        Following is example of result:
        [
            {
                "trait": "extraversion",
                "positive": true,
                "question": "Do you frequently enjoy social activities?",
                "answer": 4
            },
            {
                "trait": "extraversion",
                "positive": true,
                "question": "Do you prefer to work in teams?",
                "answer": 3
            },
            ...
        ]
    ```