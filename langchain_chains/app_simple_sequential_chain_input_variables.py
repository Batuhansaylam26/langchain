import os 
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from langchain.callbacks.tracers import ConsoleCallbackHandler

load_dotenv(find_dotenv())
# Using Langchain and prompt templates - Still Google API
llm_model = "gemini-2.0-flash"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7

)


template = """
As a children's book writer, please come up with a simple and short (90 words)
lullaby based on the location
{location}
and the main character {name}

Story:
"""
# LLM Chain
prompt = PromptTemplate(
    input_variables=["location","name"],
    template=template

)

chain = prompt | llm

story = chain.invoke(
    input={
        "location" : "Zanzibar",
        "name" : "Maya"
    },
    config={'callbacks': [ConsoleCallbackHandler()]}
)
print(
    story.content
)

print("==========================================")

story_2 = chain.invoke(
    input={
        "location" : "Emirdağ, Turkey",
        "name" : "Batuhan SAYLAM"
    },
    config={'callbacks': [ConsoleCallbackHandler()]}
)
print(
    story_2.content
)