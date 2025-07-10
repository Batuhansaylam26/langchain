from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool
from langchain.chains.llm_math.base import LLMMathChain


load_dotenv(find_dotenv())

llm= "gemini-2.0-flash"
chat = ChatGoogleGenerativeAI(
    model=llm,
    temperature=0.7
)

math_tool = Tool(
    name= "Calculator",
    func= LLMMathChain(
        llm=chat
    ),
    description="Useful for when you need to answer questions related to Math."
)

tools =[
    math_tool
]
print(
    tools[0].name,
    tools[0].description
)