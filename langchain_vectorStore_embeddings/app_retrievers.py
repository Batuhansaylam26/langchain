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
#print(len(chunks))
from langchain.vectorstores import Chroma

persist_directory = "./data/db/chroma"


os.makedirs(
    persist_directory, exist_ok= True
)

vectorStore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings

)

vectorStore.persist() #save this for later usage


#make a retriever

retriever = vectorStore.as_retriever(
    search_kwargs = {
        "k":2
    }
)

docs = retriever.get_relevant_documents(
    "Tell me more about Batuhan SAYLAM"
)

print(
    docs[0].page_content
)

#make a chain to answer

from langchain.chains.retrieval_qa.base import RetrievalQA

qa_chain  = RetrievalQA.from_chain_type(
    llm=chat,
    chain_type="stuff",
    retriever = retriever,
    verbose= True,
    return_source_documents = True
)

#Cite sources -helper function to prettyfy responses
def process_llm_response(llm_response):
    print(
        llm_response['result']
    )
    print(
        '\n\nSources:'
    )
    for source in llm_response["source_documents"]:
        print(
            source.metadata['source']
        )
    
query = "Tell me more about Batuhan SAYLAM"
llm_response = qa_chain.invoke(
    query
)

print(
    process_llm_response(
        llm_response=llm_response
    )
)








