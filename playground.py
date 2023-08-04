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
from Convo import Conversation

from langchain.prompts import PromptTemplate
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders import WebBaseLoader
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

sys.path.append('../..')
persist_directory = 'docs/chroma/'
save_dir="docs/youtube/"
openai.api_key  = os.environ['OPENAI_API_KEY']

def main():

    llm_model = "gpt-3.5-turbo"
    file = r"C:\Users\mathe\PycharmProjects\LangChainTest\Syllabi_Spring2023 (3).pdf"
    url = "https://www.youtube.com/watch?v=kWQuFmB0w-E "

    chat = Conversation(llm_model)

    chat.add_pdf_data(file)
    chat.clr_database()
    chat.add_pdf_data(file)


    while(1):
       question = input("Q: ")
       result = chat.question_n_answer(question)
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


