from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv(find_dotenv())

llm= "gemini-2.0-flash"
chat = ChatGoogleGenerativeAI(
    model=llm,
    temperature=0.7
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-exp-03-07"
)

text1 = "Kitty" #"Math is a great subject  to study."
text2 = "Rock" #"Dogs are friendly when they are happy and well fed."
text3 = "Cat" #"Physics is not one of my favorites subjects."

embed1 = embeddings.embed_query(
    text=text1
)
embed2 = embeddings.embed_query(
    text=text2
)
embed3 = embeddings.embed_query(
    text=text3
)

#print(f"Embed1 == {embed1}")

import numpy as np

similarity = np.dot(
    embed1,embed3
)
print(f"Similarity: % {similarity*100}")