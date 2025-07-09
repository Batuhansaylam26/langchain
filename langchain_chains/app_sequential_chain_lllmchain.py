from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
load_dotenv(find_dotenv())

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

prompt_story = PromptTemplate(
    input_variables=["location", "name"],
    template=template
)
chain_story = LLMChain(
    llm=llm,
    prompt=prompt_story,
    output_key= "story"
)



template_update = """
Translate the {story} into {language}. Make sure
the language is simple and fun.

Translation:
"""

prompt_translate = PromptTemplate(
    input_variables=["story", "language"],
    template=template_update
)

chain_translate = LLMChain(
    llm=llm,
    prompt=prompt_translate,
    output_key= "translated"
)


overall_chain = SequentialChain(
    chains=[chain_story,chain_translate],
    input_variables= ["location", "name","language"],
    output_variables= ["story", "translated"]
)

response = overall_chain.invoke({
    "location": "Zanzibar",
    "name": "Maya",
    "language": "Turkish"
})
print(
    f"English version ===> {response['story']}\n"
)

print(
    f"Translated version ===> {response['translated']}\n"
)