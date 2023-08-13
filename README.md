## PDF ChatBot
- Nathan Stettler
- 8/13/23 

## Setup
- clone pdf-chatbot repository
- download Python3.10
- install pipenv
- download Node.js (eventually)
- get a openai API key
- set the key to a system environment variable called OPENAI_API_KEY

## Running
- pipenv install
- pipenv run python3.10 chatbot_server.py

## Testing 
Currently, the UI is still under construction, but the API can be test via postman.
The postman collection in the repo allows a user to signup, login, add data, and chat back and forth.
- After spinning up the server, open postman on the same machine and import chatbotRequests.json.
- Send the sign-up request
- Send the upload request, after attaching a pdf to the value field of the "file" key.
- Send the start-chat request 
- Send the chat request, replacing the question in the "user_input" field with a meaningful question about the pdf uploaded. 

By sending the chat request several times with different questions you can chat with the bot. The bot generates its responses based solely on the uploaded data and the context provided by the current conversation.


