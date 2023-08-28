"""This file is for experimenting with the chatbot only and is not needed for the chatbot server"""

import os
import sys
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from chat_api.chatbot.Convo import Conversation

sys.path.append('../../../..')
persist_directory = 'docs/chroma/'
save_dir= "../../docs/youtube/"
openai.api_key  = os.environ['OPENAI_API_KEY']

def main():

    llm_model = "gpt-3.5-turbo"
    file = r"C:\Users\mathe\PycharmProjects\LangChainTest\Syllabi_Spring2023 (3).pdf"
    url = "https://www.cs.longwood.edu/"

    chat = Conversation(0,llm_model)


    chat.clr_database()

    chat.load_db()

    while(1):
       question = input("Q: ")
       result = chat.ask_question(question)
       print(result["answer"])


def load_db(file, memory, llm_model):
    loader = PyPDFLoader(file)
    documents = loader.load()

    text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    embedding = OpenAIEmbeddings()

    database = Chroma.from_documents(
        documents= chunks,
        embedding=embedding,
        persist_directory=persist_directory
    )

    retriever = database.as_retriever(search_type="mmr")

    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_model, temperature=0),
        retriever=retriever,
        memory=memory
    )
    return qa


if __name__ == '__main__':
    main()


