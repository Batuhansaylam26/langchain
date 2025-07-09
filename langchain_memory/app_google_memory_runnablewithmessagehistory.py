from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, AIMessage

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
# First we define In memory implementation of chat message history
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(
        default_factory= list,
        description = "A list of chat messages in the history."
    )
    def add_messages(self, messages: list[BaseMessage]) -> None:
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = list() 



# Here we use a global variable to store the chat message history.
# This will make it easier to inspect it to see the underlying results.
store = {}


def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]



prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name='history'),
    ("human", "{input}")
])


chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history= get_by_session_id,
    input_messages_key= "input",
    history_messages_key= "history"
)

print(
    chain_with_history.invoke(
        {
            "input" : message,
        },
        config={"configurable": {"session_id": "foo"}}
    )
)

print(
    chain_with_history.invoke(
        {
            "input" : message_2
        },
        config={"configurable": {"session_id": "foo"}}
    )
)

print("=========================================================")

print(
    chain_with_history.get_session_history("foo")
)