from langchain.chains.llm import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

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

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose= True

)

story = chain.invoke(
    {
        "location" : "Zanzibar",
        "name" : "Maya"
    }
)
print(
    story['text']
)

print("==========================================")

story_2 = chain.invoke(
    {
        "location" : "Emirdağ, Turkey",
        "name" : "Batuhan SAYLAM"
    }
)
print(
    story_2['text']
)