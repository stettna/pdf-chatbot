
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

class Conversation:

    def __init__(self, llm):
        self.persist_directory = 'docs/chroma/'
        self.save_dir = "docs/youtube/"
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.embedding = OpenAIEmbeddings()
        self.database = None
        self.qa = None
        self.llm_model = llm


    def clr_database(self):

        if self.database != None:
            self.database.delete_collection()
            self.database = None

        return


    def add_pdf_data(self, file):

        loader = PyPDFLoader(file)
        documents = loader.load()

        chunks = self.split_data(documents, 100, 25)

        if self.database is None:
            self.database = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding,
                persist_directory=self.persist_directory
            )

        else:
            self.database.add_documents(documents)

        self.load_db()

        return


    def add_YT_data(self, url):

        loader = GenericLoader(
            YoutubeAudioLoader([url], self.save_dir),
            OpenAIWhisperParser()
        )

        documents = loader.load()

        chunks = self.split_data(documents, 300, 75)

        if self.database is None:
            self.database = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding,
                persist_directory=self.persist_directory
            )
        else:
            self.database.add_documents(documents)

        self.load_db()

        return


    def question_n_answer(self, question):

        if self.qa is None:
            return

        return self.qa({"question" : question})


    def split_data(self, documents, size, overlap):

        text_splitter = TokenTextSplitter(chunk_size=size, chunk_overlap=overlap)
        chunks = text_splitter.split_documents(documents)

        return chunks


    def load_db(self):

        retriever = self.database.as_retriever(search_type="mmr")

        self.qa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name=self.llm_model, temperature=0),
            retriever=retriever,
            memory=self.memory
        )

        return
