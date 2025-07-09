from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import find_dotenv, load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain
load_dotenv(find_dotenv())
# Using Langchain and prompt templates - Still Google API
llm_model = "gemini-2.0-flash"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7

)

message = "My name is Batuhan. What is yours?"

message_2 = "Great! What is my name?"

print(
    llm.invoke(
        message
    ).content
)

print(
    llm.invoke(
        message_2
    ).content
)

# How to solve llms memory issues?
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm= llm,
    memory=memory,
    verbose=True
)

conversation.invoke(
    input= message
)

conversation.invoke(
    input= message_2
)

print(
    memory.load_memory_variables({})
)