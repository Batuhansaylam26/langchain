# Langchain 

First of al, on the [app.py](app.py), The chains are used by using basic prompt template and the huggingface distilgpt2 and API , which is on the .env,  to understane how to use the **langchain** basicly.

![Prompt Template & LLM - Chain [4]](images/1_4wwDs1_d6B42FQTl-dB9pw.png)

Then, The Gemini-2.5-Flash was used by using kwarg after the GOOGLE_API_KEY was generated and declared as environment variables on .env.

## [Prompt Templates](langchain_prompt_template)

> Prompt templates help to translate user input and parameters into instructions for a language model. This can be used to guide a model's response, helping it understand the context and generate relevant and coherent language-based output [1].<br>

By using claude-opus-4 and Gemini-2.5-Flash (both google api and langchain_google_genai), converted the customer reviews into tones and languages which was given as input. 

## [Structured Output Parsers](langchain_output_parser)
### [Dictionary Parser](langchain_output_parser/app_langchain_google_api_langchain_parser.py)
Firstly, on **Dictionary parser**, A list which includes the keys of information, we want to extract from messages and declared by using [ResponseSchema](https://python.langchain.com/api_reference/langchain/output_parsers/langchain.output_parsers.structured.ResponseSchema.html) with their descriptions and names, is created. After that, An output parser which gives us JSON was declared by giving the list of response shemas as input. Then, the output parser was given in the prompt template during formating messages. Finally, the content of the output of the chat model was parsing by using output parser which we declared. <br>

![Pipeline of output parser [5]](images/1_cFS4aWCi4FnKcnk1xu5Gqw.png)

### [Pydantic Parser](langchain_output_parser/app_langchain_google_pydantic_parser.py)

Instead of using ResponseShema, Pydantic [Base model class](https://docs.pydantic.dev/latest/api/base_model/) was used to extract information. This provides us validation of fields which are declared in the class.<br>

## Memory & Chains
### [Memory](langchain_memory)
> Memory maintains Chain state, incorporating context from past runs.[2]<br>

Since the models are statless, the memories are needed. There are several types of memory. <br>

![Memory[3]](images/0_sUkvbURF633MXJyX.png)
#### [Conversation Buffer Memory](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.buffer.ConversationBufferMemory.html)
This type of memory allows for storing of message and then extract the messages in a variable.<br>
#### [Conversation Buffer Window memory](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.buffer_window.ConversationBufferWindowMemory.html)
This memory keeps a list of interactions of the conversation over time. It only uses the last k interactions.<br>
#### [Conversation Token Buffer Memory](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.token_buffer.ConversationTokenBufferMemory.html)
This memory keeps a buffer of recent interactions in memory and uses token length rather than the number of interactions to determine when to flush interactions.<br>


Firstly, The Conversation buffer memory was applied on [the script](langchain_memory/app_google_memory_ConversationBufferMemory.py). On this script, after the declareation of chat model and memory, they was wrapped by Conversation chain.<br>

All memory types had been changed. Memory were deprecated. Insted of this, use <ins>history</ins>. <br>

In order to apply history on [the script](langchain_memory/app_google_memory_runnablewithmessagehistory.py), firstly, a class which inherits from pydantic Base model and BaseChatMessageHistory was created. The attribute of the class which is a list is messages. The attribute contains the human, asistant and system messages as a BaseMessage. Then, the objects initialized from the class are stored by session id in dictionary. <br>

Prompts are made by messages and the history message key is given to the prompt as message placeholder. After the chain is constructed by chat model and prompt, the RunnableWithMessageHistory is initialized by the necessary parameters. Then, the chain with history can be invoked by using session id as configurable and an input.<br>

### [Chain](langchain_chains)





# References
[1] https://python.langchain.com/docs/concepts/prompt_templates/ <br>
[2] https://python.langchain.com/api_reference/langchain/memory.html <br>
[3] https://images.app.goo.gl/sx5FcTgNzoaQKroz6 <br>
[4] https://images.app.goo.gl/wZvEEapCLpqJMw5w5 <br>
[5] https://images.app.goo.gl/TxXnsJTQhCYnSwKeA <br>