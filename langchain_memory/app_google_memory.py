from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv(find_dotenv())
# Using Langchain and prompt templates - Still Google API
llm_model = "gemini-2.0-flash"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7

)