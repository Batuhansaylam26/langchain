from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory

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
prompt = ChatPromptTemplate.from_messages([
    ("placeholder", "{history}"), # This is where the conversation history will be injected
    ("human", "{input}")
])
# How to solve llms memory issues?
memory = ConversationBufferMemory()

# 2. Initialize ConversationBufferMemory
# This memory stores messages in a buffer.
store = {} # A simple dictionary to store memory for different session_ids

def get_session_history(session_id: str) -> ConversationBufferMemory:
    if session_id not in store:
        store[session_id] = memory
    return store[session_id]

# 3. Create RunnableWithMessageHistory
# This wraps your LLM and handles memory management.
conversation = RunnableWithMessageHistory(
    llm=llm,
    get_session_history=get_session_history, # Use the callable to get history for a session
    verbose=True, # Set to True to see what LangChain is doing
    runnable=prompt # Pass your prompt template here

)


print(
    conversation.invoke(
        input = message,
        config={"configurable": {"session_id": "user123"}}
    ).content
)

print(
    conversation.invoke(
        input = message_2,
        config={"configurable": {"session_id": "user123"}}
    ).content
)