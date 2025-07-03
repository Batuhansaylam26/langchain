from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import PromptTemplate


load_dotenv(find_dotenv())

llm_model = "gemini-2.0-flash"
kwargs ={
    "max_output_tokens" : 2000,
    "tokenizer" : False
}
llm = ChatGoogleGenerativeAI(
    model=llm_model,
    model_kwargs=kwargs
)



# Prompt template oluşturuyoruz
template = """Question: {question}
Answer: Let's think step by step.""" 
prompt_template = PromptTemplate.from_template(
    template
)


# Zinciri oluşturup çağırıyoruz
chain = prompt_template | llm

question = "Who is the president of US?" 
print(
    chain.invoke(
        {"question": question})\
            .content 
)


