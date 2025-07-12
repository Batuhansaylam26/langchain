from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, load_tools
from langchain.chains.llm_math.base import LLMMathChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

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

prompt = PromptTemplate(
    input_variables=["query"],
    template="{query}"
)

llm_chain = LLMChain(
    llm=chat,
    prompt=prompt
)

#Inıtialize LLM tool
llm_tool = Tool(
    name = "Language Model",
    func=llm_chain.run,
    description="Use this tool for general queries and logic."
)



tools = load_tools(
    ['llm-math'],
    llm=chat
)

tools.append(llm_tool)

agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=chat,
    verbose=True,
    max_iterations=3 #to avoid high bills from the LLM
)


query = "What is the capital of China?"
result = agent.invoke(query)


print(
    result['output']
)

query2 = "If James is currently 45 years old, how old will he be in 50 years? \
    If he has 4 kids and adopted 7 more, how many children does he have?"
result2 = agent.invoke(query2)


print(
    result2['output']
)