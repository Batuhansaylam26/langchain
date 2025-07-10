from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import PyPDFLoader


load_dotenv(find_dotenv())

chat = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)


loader = PyPDFLoader("./data/Batuhan Saylam Resume.pdf")

pages = loader.load()

print(len(pages))

page = pages[0]

print(page.page_content[0:50])