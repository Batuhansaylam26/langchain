from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv(find_dotenv())

chat = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)


with open("./data/letter_of_intent.txt", encoding='iso-8859-9') as paper:
    resume = paper.read()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 20,
    chunk_overlap = 3,
    length_function = len
)

texts = text_splitter.create_documents([resume])

print(
    texts
)