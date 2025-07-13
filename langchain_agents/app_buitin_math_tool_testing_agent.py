from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, load_tools
from langchain.chains.llm_math.base import LLMMathChain


load_dotenv(find_dotenv())

llm= "gemini-2.0-flash"
chat = ChatGoogleGenerativeAI(
    model=llm,
    temperature=0.7
)


tools = load_tools(
    ['llm-math'],
    llm=chat
)
"""print(
    tools[0].name,
    tools[0].description
)"""

agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=chat,
    verbose=True,
    max_iterations=3 #to avoid high bills from the LLM
)
query = "What is 3.1**2.1"
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

query2 = "What is the capital of Mozambique"
result2 = agent.invoke(query2)


print(
    result2['output']
)
"""
> Entering new AgentExecutor chain...
I don't have the tools to answer factual questions about geography. I am an AI assistant that can only use the calculator tool.
Final Answer: I am sorry, I cannot answer this question.

> Finished chain.
I am sorry, I cannot answer this question.
"""