from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_core.output_parsers import StrOutputParser

def generate_lullaby(location,name,language):
    load_dotenv(find_dotenv())

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7
    )

    template = """
    As a children's book writer, please come up with a simple and short (90 words)
    lullaby based on the location
    {location}
    and the main character {name}

    Story:
    """

    prompt_story = PromptTemplate(
        input_variables=["location", "name"],
        template=template
    )
    chain_story = prompt_story | llm | StrOutputParser()
    template_update = """
    Translate the {story} into {language}. Make sure
    the language is simple and fun.

    Translation:
    """

    prompt_translate = PromptTemplate(
        input_variables=["story", "language"],
        template=template_update
    )

    chain_translate = prompt_translate | llm |  StrOutputParser()



    overall_chain = RunnableSequence(
        # Step 1: Prepare the inputs for the entire process.
        # This RunnableParallel takes the initial inputs (location, name, language).
        # It runs 'chain_story' to get the English story, and passes 'language' through.
        # Output of this step: {"story": "English Lullaby", "language": "Target Language"}
        RunnableParallel(
            story=chain_story, # This will execute chain_story using initial 'location' and 'name'
            language = lambda x: x['language'] # Passes the initial 'language' input directly
        ),
        # Step 2: Take the output from Step 1 (which is {"story": ..., "language": ...})
        # and use it to generate the translation, while preserving the original story.
        # Output of this step: {"story": "English Lullaby", "translated": "Translated Lullaby"}
        RunnableParallel(
            # The 'story' key here simply takes the 'story' value from the input of this step (x).
            # This ensures the original English story is part of the final output.
            story=lambda x: x["story"],
            # The 'translated' key defines how the translated text is generated.
            # It uses a sub-chain that explicitly maps 'story' and 'language' from 'x'
            # to the 'chain_translate' runnable.
            translated= chain_translate # Execute the translation chain with the mapped inputs
        )
    )

    response = overall_chain.invoke({
        "location": location,
        "name": name,
        "language": language
    })

    return response