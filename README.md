## PDF ChatBot
- Nathan Stettler
- 8/13/23 

## About the App
This app allows users to submit their own data in the form of a PDF, and then asks questions of chat-bot about the data. 
The chat-bot creates responses solely based on the data submitted and any context given during the conversation. The app
uses the flask framework for the backend, react.js for the UI, langchain to communicate with OpenAI's gpt

Users can create an account with a username and password. Associated with each account is vector store that is persisted
in memory, allowing users to return to their already submitted data in their next chat session. The app also provides a 
way to clear the vector-store for a fresh database.

## Setup
- clone pdf-chatbot repository
- download Python3.10
- install pipenv
- download Node.js
- get an openai API key
- set the key to a system environment variable called OPENAI_API_KEY

## Running
- pipenv install
- pipenv run python3.10 chatbot_server.py
- cd chat-app
- npm install
- npm start

## Using
- After spinning up the server and loading the UI, click the link, create an account, and hit submit.
- Upload any PDF files you wish to inquire about
- Press chat, and begin asking questions. The bot will do its best to answer them.
- The end chat button takes you back to the upload page where you can modify your database again

WARNING: Refreshing the page with send you back to the login screen, so this is not recommended during a conversation

## Helpful Sources
- https://learn.deeplearning.ai/langchain-chat-with-your-data/lesson/1/introduction
- https://www.youtube.com/watch?v=dam0GPOAvVI&t=1468s
- https://www.youtube.com/watch?v=Y-XW9m8qOis


