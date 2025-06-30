import os 
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM # AutoModelForCausalLM'i kullanıyoruz
from dotenv import find_dotenv, load_dotenv
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEndpoint
load_dotenv( 
    find_dotenv() 
)


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
from langchain_core.prompts import PromptTemplate
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