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
from langchain.document_loaders import WebBaseLoader

class Conversation:

    def __init__(self, id, llm, size=100, overlap=20):
        self.id = id #user id
        self.size = size #size of split data
        self.overlap = overlap #amount of overlap on each chunk of data
        self.persist_directory = 'uploads/' + str(id) + '/chroma'
        self.save_dir = "uploads/" + str(id)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.embedding = OpenAIEmbeddings()
        self.vector_store = None
        self.chatbot = None
        self.llm_model = llm


    def clr_database(self):
        #clears existing vector store of data
        if self.vector_store != None:
            self.vector_store.delete_collection()
            self.vector_store = None

        return


    def add_pdf_data(self, file):

        loader = PyPDFLoader(file)
        documents = loader.load() #loads docuemnts created from PDF

        chunks = self.split_data(documents, self.size, self.overlap) #divids documents into chunks

        if self.vector_store is None: #if None create vector, store then add chunks to it
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding,
                persist_directory=self.persist_directory
            )

        else:
            self.vector_store.add_documents(documents)

        return


    def add_YT_data(self, url):

        loader = GenericLoader(
            YoutubeAudioLoader([url], self.save_dir),
            OpenAIWhisperParser()
        )

        documents = loader.load()

        chunks = self.split_data(documents, 300, 75)

        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding,
                persist_directory=self.persist_directory
            )
        else:
            self.vector_store.add_documents(documents)

        return


    def add_web_data(self, url):

        loader = WebBaseLoader(url)

        documents = loader.load()

        chunks = self.split_data(documents, self.size, self.overlap)

        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding,
                persist_directory=self.persist_directory
            )
        else:
            self.vector_store.add_documents(documents)

        return


    def ask_question(self, question):

        if self.chatbot is None:#should never happen
            return

        return self.chatbot({"question": question}) #asks question and returns chatbot response


    def split_data(self, documents, size, overlap):

        #splits data by tokens
        text_splitter = TokenTextSplitter(chunk_size=size, chunk_overlap=overlap)
        chunks = text_splitter.split_documents(documents)

        return chunks


    def load_db(self):

        if self.vector_store is None: #if none create it
            self.vector_store = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding)

        # creates retriever to get relavent content from database
        retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={'k': 3, 'fetch_k': 15})

        #creates conversation chain with llm
        self.chatbot = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name=self.llm_model, temperature=0),
            retriever=retriever,
            memory=self.memory,
        )

        return
