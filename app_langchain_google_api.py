from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import PromptTemplate
from google import genai
from google.genai import types
load_dotenv(find_dotenv())

llm_model = "gemini-2.0-flash"


client = genai.Client()
"""
chat_model = client.chats.create(
    model = llm_model,
    config = types.GenerationConfig(
        temperature=0.7,
    ),
    history=types.Content(
        role="user", 
        parts=[
            types.Part(
                text="Hello"
            )
        ]
    )
)"""
def get_completion(prompt, model=llm_model):
    chat = client.chats.create(
        model = llm_model,
        config = types.GenerateContentConfig(
            temperature=0.7,
        )
    )
    response = chat.send_message(prompt)
    return response.text


#translate text, review

customer_review = """
    Your product is terrible! I do not know how 
    you were able to get this the market.
    I do not want this! Actually no one should want this.
    Seriously! Give me money now!
"""

tone = """ Proper British English in a nice, warm, respectful tone"""
language = """Turkish"""
prompt = f"""
    Rewrite the following {customer_review} message in {tone}, and then
    please translate the new review message into {language}.
"""

rewrite = get_completion(prompt=prompt)

print(rewrite)