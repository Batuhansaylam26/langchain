from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import os

load_dotenv(find_dotenv())

llm= "gemini-2.0-flash"
chat = ChatGoogleGenerativeAI(
    model=llm,
    temperature=0.7
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

#Loading document
loader = PyPDFLoader("./data/Batuhan Saylam Resume.pdf")

docs = loader.load()
#Split doc into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 150
)

chunks = text_splitter.split_documents(docs)
#Saving chunks
#Chroma DB 
print(len(chunks))
from langchain.vectorstores import Chroma

persist_directory = "./data/db/chroma"


os.makedirs(
    persist_directory, exist_ok= True
)

vectorStore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_directory

)

"""print(
    vectorStore._collection.count()
)
"""
query = "What is Batuhan's education?"

docs_resp = vectorStore.similarity_search(
    query=query,
    k=3
)

print(len(docs_resp))

print("=======================================================")


print(docs_resp[0].page_content)















