from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv(find_dotenv())
# Using Langchain and prompt templates - Still Google API
llm_model = "gemini-2.0-flash"


chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7

)
#translate text, review

customer_review = """
    Your product is terrible! I do not know how 
    you were able to get this the market.
    I do not want this! Actually no one should want this.
    Seriously! Give me money now!
"""

template_string = """
    Translate the follwing text {customer_review} 
    into italiano in polite tone.
    And the company name is {company_name}
"""

prompt_template = ChatPromptTemplate.from_template(
    template = template_string
)

translation_message = prompt_template.format_messages(
    customer_review = customer_review,
    company_name = "Google"
)

response = chat_model(translation_message)

print(response.content)