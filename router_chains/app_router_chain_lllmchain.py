from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain.chains.llm import LLMChain


load_dotenv(find_dotenv())

chat = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)

biology_template = """
You are a very smart biology professor.
You are great at answering questions about biology in a concise and easy to understand.
When you do not know the answer to a question you admit that you don't know.

Here is a question:
{input}
"""

math_template = """
You are a very good mathematician.
You are great at answering questions about mathematics in a concise and easy to understand.
You are so good because you are able to break down hard problems into their components and 
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{input}
"""
astronomy_template = """
You are a very good astronomer.
You are great at answering questions about astronomy in a concise and easy to understand.
You are so good because you are able to break down hard problems into their components and 
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{input}
"""

travel_agent_template = """
You are a very good travel agent with a large amount
of knowledge when it comes to getting people the best deals and recommendations
for travel, vacations, flights and world's best destination for vacation.
You are so good because you are able to break down hard problems into their components and 
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{input}
"""

prompt_infos = [
    {
        "name" : "Biology",
        "description" : "Good for answering Biology related questions",
        "prompt_template" : biology_template
    },
    {
        "name" : "math",
        "description" : "Good for answering math questions",
        "prompt_template" : math_template
    },
    {
        "name" : "astronomy",
        "description" : "Good for answering astronomy questions",
        "prompt_template" : astronomy_template
    },
    {
        "name" : "travel_agent",
        "description" : "Good for answering travel, tourism and vacation questions",
        "prompt_template" : travel_agent_template
    }
]

destination_chains = dict()

for info in prompt_infos:
    name = info["name"]
    prompt_template = info["prompt_template"]
    prompt = ChatPromptTemplate.from_template(
        template=prompt_template
    )

    chain = LLMChain(
        llm=chat,
        prompt=prompt
    )
    destination_chains[name] = chain


default_prompt = ChatPromptTemplate.from_template(
    "{input}"
)

default_chain  = LLMChain(
    llm=chain,
    prompt=default_prompt
)


from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router import MultiPromptChain
destinations =[f"{p["name"]}: {p["description"]}" for p in prompt_infos]


destinations_str = "\n".join(destinations)


router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    destinations=destinations_str
)

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser()
)


router_chain = LLMRouterChain.from_llm(
    llm=chat,
    prompt=router_prompt
)

chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=default_chain,
    verbose=True
)

response = chain.run(
    "I need to got to Kenya for vacation, a family of four"
)


print(response)