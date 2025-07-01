import os 
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM # AutoModelForCausalLM'i kullanıyoruz
from dotenv import find_dotenv, load_dotenv
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEndpoint
load_dotenv( 
    find_dotenv() 
)
from langchain_huggingface import ChatHuggingFace
from langchain_core.prompts import PromptTemplate

# Hugging Face API token'ına bu senaryoda doğrudan ihtiyacımız yok
# çünkü model yerel olarak çalışacak.

# Metin üretimi yapabilen bir modeli seçiyoruz (örn: distilgpt2)
model_id = "distilgpt2" 

# Tokenizer ve modeli yüklüyoruz (CausalLM yani metin üretimi için olanı)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Metin üretimi pipeline'ını oluşturuyoruz
# Varsayılan olarak "text-generation" görevi için AutoModelForCausalLM kullanılır.
pipe = pipeline(
    "text-generation", 
    model=model, 
    tokenizer=tokenizer, 
    max_new_tokens=100, 
    top_k=50, 
    temperature=0.7 # Yerel modelde daha yüksek sıcaklıklar deneyebiliriz
)

# LangChain HuggingFacePipeline'ı başlatıyoruz
llm = HuggingFacePipeline(pipeline=pipe) 

question = "Who is the president of US?" 

# Prompt template oluşturuyoruz
template = """Question: {question}
Answer: Let's think step by step.""" # distilgpt2 genellikle cevabı tamamlar, "Let's think step by step" ona uymayabilir.
prompt_template = PromptTemplate.from_template(template)

# Zinciri oluşturup çağırıyoruz
chain = prompt_template | llm

print(
    chain.invoke({"question": question}) 
)

#or by using Huggingface end point
"""HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
llm_endpoint = HuggingFaceEndpoint(
    repo_id=model_id,
    max_new_tokens=100,
    temperature=0.7,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)


llm_chain = prompt_template | llm_endpoint
print(llm_chain.invoke({"question": question}))"""


#We can also use chat models
# And also we can use hugginface pipeline directly

chat_model_id = "distilgpt2"
chat_llm = HuggingFacePipeline.from_model_id(
    model_id=chat_model_id,
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        tokenizer = False
    ),
)


chat_model = ChatHuggingFace(llm=chat_llm)


chat_question = "Who is the president of US?" 

# Prompt template oluşturuyoruz
chat_template = """Question: {question}
Answer: Let's think step by step.""" # distilgpt2 genellikle cevabı tamamlar, "Let's think step by step" ona uymayabilir.
chat_prompt_template = PromptTemplate.from_template(chat_template)

# Zinciri oluşturup çağırıyoruz
chain_chat = chat_prompt_template | chat_model

print(
    chain_chat.invoke({"question": chat_question}) 
)


