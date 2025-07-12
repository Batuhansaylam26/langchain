from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import  initialize_agent, Tool
from langchain_community.utilities import SerpAPIWrapper
import os

load_dotenv(find_dotenv())

llm= "gemini-2.0-flash"
chat = ChatGoogleGenerativeAI(
    model=llm,
    temperature=0.7
)

serp_api_key = os.getenv(
    "SERP_API_KEY"
)

search = SerpAPIWrapper(
    serpapi_api_key=serp_api_key
)
# --- Tüm Araçları Bir Listede Toplama ---
tools = [
    Tool(
        name="Intermediate Answer",
        func = search.run,
        description=  "Google Search"
    )
]

self_ask_with_agent = initialize_agent(
    tools,
    chat, # LLM nesnesini buraya geçirin
    agent="self-ask-with-search", # Doğru agent tipi
    verbose=True
)

# --- Sorguyu Çalıştırma ---
query = "How to bake a cake with  123 ingradients?"
result = self_ask_with_agent.invoke(query) # Ajanlar için invoke metodunu ve dict input'u kullanın

print("\n--- Nihai Cevap ---")
print(result['output'])

"""print(
    self_ask_with_agent.agent.llm_chain.prompt.template
)"""