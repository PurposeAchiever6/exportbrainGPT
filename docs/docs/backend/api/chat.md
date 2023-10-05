---
sidebar_position: 2
---

# Chat system

**URL**: https://api.quivr.app/chat

**Swagger**: https://api.quivr.app/docs

## Overview

Users can create multiple chat sessions, each with its own set of chat messages. The application provides endpoints to perform various operations such as retrieving all chats for the current user, deleting specific chats, updating chat attributes, creating new chats with initial messages, adding new questions to existing chats, and retrieving the chat history. These features enable users to communicate and interact with their data in a conversational manner.

1. **Retrieve all chats for the current user:**

   - HTTP method: GET
   - Endpoint: `/chat`
   - Description: This endpoint retrieves all the chats associated with the current authenticated user. It returns a list of chat objects containing the chat ID and chat name for each chat.

2. **Delete a specific chat by chat ID:**

   - HTTP method: DELETE
   - Endpoint: `/chat/{chat_id}`
   - Description: This endpoint allows deleting a specific chat identified by its chat ID.

3. **Update chat attributes:**

   - HTTP method: PUT
   - Endpoint: `/chat/{chat_id}/metadata`
   - Description: This endpoint is used to update the attributes of a chat, such as the chat name.

4. **Create a new chat with initial chat messages:**

   - HTTP method: POST
   - Endpoint: `/chat`
   - Description: This endpoint creates a new chat with initial chat messages. It expects the chat name in the request payload.

5. **Add a new question to a chat:**

   - HTTP method: POST
   - Endpoint: `/chat/{chat_id}/question`
   - Description: This endpoint allows adding a new question to a chat. It generates an answer for the question using different models based on the provided model type.

   Models like gpt-4-0613 and gpt-3.5-turbo-0613 use a custom OpenAI function-based answer generator.
   ![Function based answer generator](../../../static/img/answer_schema.png)

6. **Get the chat history:**
   - HTTP method: GET
   - Endpoint: `/chat/{chat_id}/history`
   - Description: This endpoint retrieves the chat history for a specific chat identified by its chat ID.
