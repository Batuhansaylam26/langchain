from langchain.chains.llm import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder


load_dotenv(find_dotenv())
# Using Langchain and prompt templates - Still Google API
llm_model = "gemini-2.0-flash"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7

)
# LLM Chain
prompt = PromptTemplate(
    input_variables=["language"],
    template="How do you say good morning in {language}"

)

chain = LLMChain(
    llm=llm,
    prompt=prompt

)


print(
    chain.run(
        language = "French"
    )
)

print("==========================================")


print(
    chain.run(
        language = "Portugese"
    )
)
