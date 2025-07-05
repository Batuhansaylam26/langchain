from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv(find_dotenv())
# Using Langchain and prompt templates - Still Google API
llm_model = "gemini-2.0-flash"


chat = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7

)
#translate text, review

email_response = """
Here's our itinerary for our upcoming trip to Europe.
We leave from Denver, Colorado airport at 8:45 pm, and arrive in Amsterdam 10 hours 
at Schipol Airport.
We'll grab a ride to our airbnb and maybe stop somewhere for breakfast before 
taking a nap.

Some sightseeing will follow for a couple of hours.
we will then go shop for gifts
to bring back to our children and friends.

The next morning, at 7:45 am we'll drive to to Belgium, Brussels.
While in Brussels we want to explore the city to its fullest.
"""
email_template = """
From the following email, extract the following information:
leave_time: when are they leaving for vacation to Europe. If there's an actual
time written, use it, if not write unknown.

leave_from: where are they leaving from, the airport or city name and state if available.

cities_to_visit: extract the cities they are going to visit. If there are more than one, put them in square brackets like '["cityone","citytwo"]'.

Format the output as JSON with the following keys:
leave_time
leave_from
cities_to_visit

email: {email}
"""
prompt_template = ChatPromptTemplate.from_template(
    template = email_template
)
#print(prompt_template)

messages = prompt_template.format_messages(
    email = email_response,
)
response = chat.invoke(input=messages)

print(type(response.content))


from langchain.output_parsers import ResponseSchema, StructuredOutputParser


leave_time_schema = ResponseSchema(
    name= "leave_time",
    description= "When they are leaving. \
        It's usually a numerical time of the day. \
             If not available write n/a "
)


leave_from_schema = ResponseSchema(
    name= "leave_from",
    description= "Where they are leaving. \
        It's a city, airport or state, or province"
)


cities_to_visit_schema = ResponseSchema(
    name= "cities_to_visit",
    description= "The cities, towns they will be visiting during their trip. \
        This needs to be in a list"
)

response_schema = [
    leave_time_schema,
    leave_from_schema,
    cities_to_visit_schema
]


# setup the output parser

output_parser = StructuredOutputParser.from_response_schemas(
    response_schemas=response_schema
)

format_instructions = output_parser.get_format_instructions()

#print(format_instructions)
# reviewed email template - we update to add the {format_instructions}
email_template_revised = """
From the following email, extract the following information:
leave_time: when are they leaving for vacation to Europe. If there's an actual
time written, use it, if not write unknown.

leave_from: where are they leaving from, the airport or city name and state if available.

cities_to_visit: extract the cities they are going to visit. If there are more than one, put them in square brackets like '["cityone","citytwo"]'.

Format the output as JSON with the following keys:
leave_time
leave_from
cities_to_visit

email: {email}
{format_instructions}
"""


updated_prompt = ChatPromptTemplate.from_template(
    template=email_template_revised
)

messages = prompt_template.format_messages(
    email = email_response,
    format_instructions = format_instructions
)

response = chat.invoke(messages)



output_dict = output_parser.parse(
    response.content
) # parse into dict

print(output_dict)
print(type(output_dict))

print(
    f" \
Cities:::: {output_dict['cities_to_visit'][0]} \
    "
)