from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import PromptTemplate
import anthropic
from google.genai import types


load_dotenv(find_dotenv())

llm_model = "claude-opus-4-20250514"


client = anthropic.Anthropic()

def get_completion(prompt, model=llm_model):
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=0.7,
        #system="You are a world-class poet. Respond only with short poems.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return response.content


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