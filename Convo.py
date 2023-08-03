import os
import sys
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

class Conversation:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.embedding = OpenAIEmbeddings()


    def clr_database(self):
        ...


    def add_pdf_data(self, file):

        loader = PyPDFLoader(file)
        documents = loader.load()
        self.database.add_documents(documents)
        return


    def add_YT_data(self):
        ...


    def ask_question(self):
        ...


    def get_answer(selfself):
        ...


    def split_data(self, documents, size, overlap):

        text_splitter = TokenTextSplitter(chunk_size=size, chunk_overlap=overlap)
        chunks = text_splitter.split_documents(documents)

        return chunks


    def load_db(file, memory, llm_model):


        retriever = database.as_retriever(search_type="mmr")

        qa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name=llm_model, temperature=0),
            retriever=retriever,
            memory=memory
        )
        return qa
