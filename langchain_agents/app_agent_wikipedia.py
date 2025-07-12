from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import  initialize_agent
from langchain_community.tools import WikipediaQueryRun # Wikipedia'yı arama aracı olarak kullanmak için
from langchain_community.utilities import WikipediaAPIWrapper # WikipediaQueryRun için wrapper


load_dotenv(find_dotenv())

llm= "gemini-2.0-flash"
chat = ChatGoogleGenerativeAI(
    model=llm,
    temperature=0.7
)



wikipedia_api_wrapper = WikipediaAPIWrapper(
    top_k_results=1,           # Tek bir en iyi sonucu al
    doc_content_chars_max=4000 # Gelen belge içeriğinin maksimum karakter sayısı
)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)

# --- Tüm Araçları Bir Listede Toplama ---
tools = [
    wikipedia_tool # Doğrudan Wikipedia aracını ekledik
]

wikipedia_agent = initialize_agent(
    tools,
    chat, # LLM nesnesini buraya geçirin
    agent="zero-shot-react-description", # Doğru agent tipi
    verbose=True,
    max_iterations=5 # İterasyon sayısını artırmak karmaşık sorgulara yardımcı olabilir
)

# --- Sorguyu Çalıştırma ---
query = "What was Bach's last piece he wrote?"
result = wikipedia_agent.invoke({"input": query}) # Ajanlar için invoke metodunu ve dict input'u kullanın

print("\n--- Nihai Cevap ---")
print(result['output'])

print(
    wikipedia_agent.agent.llm_chain.prompt.template
)