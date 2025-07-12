# Langchain 

First of al, on the [app.py](app.py), The chains are used by using basic prompt template and the huggingface distilgpt2 and API , which is on the .env,  to understane how to use the **langchain** basicly.

![Prompt Template & LLM - Chain [4]](images/1_4wwDs1_d6B42FQTl-dB9pw.png)

Then, The Gemini-2.5-Flash was used by using kwarg after the GOOGLE_API_KEY was generated and declared as environment variables on .env.

## [Prompt Templates](langchain_prompt_template)

> Prompt templates help to translate user input and parameters into instructions for a language model. This can be used to guide a model's response, helping it understand the context and generate relevant and coherent language-based output [1].<p>

By using claude-opus-4 and Gemini-2.5-Flash (both google api and langchain_google_genai), converted the customer reviews into tones and languages which was given as input. <p>

## [Structured Output Parsers](langchain_output_parser)
### [Dictionary Parser](langchain_output_parser/app_langchain_google_api_langchain_parser.py)
Firstly, on **Dictionary parser**, A list which includes the keys of information, we want to extract from messages and declared by using [ResponseSchema](https://python.langchain.com/api_reference/langchain/output_parsers/langchain.output_parsers.structured.ResponseSchema.html) with their descriptions and names, is created. After that, An output parser which gives us JSON was declared by giving the list of response shemas as input. Then, the output parser was given in the prompt template during formating messages. Finally, the content of the output of the chat model was parsing by using output parser which we declared. <p>

![Pipeline of output parser [5]](images/1_cFS4aWCi4FnKcnk1xu5Gqw.png)

### [Pydantic Parser](langchain_output_parser/app_langchain_google_pydantic_parser.py)

Instead of using ResponseShema, Pydantic [Base model class](https://docs.pydantic.dev/latest/api/base_model/) was used to extract information. This provides us validation of fields which are declared in the class.<p>

## Memory & Chains
### [Memory](langchain_memory)
> Memory maintains Chain state, incorporating context from past runs.[2]<p>

Since the models are statless, the memories are needed. There are several types of memory. <p>

![Memory[3]](images/0_sUkvbURF633MXJyX.png)
#### [Conversation Buffer Memory](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.buffer.ConversationBufferMemory.html)
This type of memory allows for storing of message and then extract the messages in a variable.<p>
#### [Conversation Buffer Window memory](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.buffer_window.ConversationBufferWindowMemory.html)
This memory keeps a list of interactions of the conversation over time. It only uses the last k interactions.<p>
#### [Conversation Token Buffer Memory](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.token_buffer.ConversationTokenBufferMemory.html)
This memory keeps a buffer of recent interactions in memory and uses token length rather than the number of interactions to determine when to flush interactions.<p>


Firstly, The Conversation buffer memory was applied on [the script](langchain_memory/app_google_memory_ConversationBufferMemory.py). On this script, after the declareation of chat model and memory, they was wrapped by Conversation chain.<p>

All memory types had been changed. Memory were deprecated. Insted of this, use <ins>history</ins>. <p>

In order to apply history on [the script](langchain_memory/app_google_memory_runnablewithmessagehistory.py), firstly, a class which inherits from pydantic Base model and BaseChatMessageHistory was created. The attribute of the class which is a list is messages. The attribute contains the human, asistant and system messages as a BaseMessage. Then, the objects initialized from the class are stored by session id in dictionary. <p>

Prompts are made by messages and the history message key is given to the prompt as message placeholder. After the chain is constructed by chat model and prompt, the RunnableWithMessageHistory is initialized by the necessary parameters. Then, the chain with history can be invoked by using session id as configurable and an input.<p>

### [Chain](langchain_chains)

>Chains are easily reusable components linked together.<br>
Chains encode a sequence of calls to components like models, document retrievers, other Chains, etc., and provide a simple interface to this sequence [6].<p>


The types which are in the repo, the simple sequential, sequential and router. Both langchain expression language and llmchain versions were applied.<p>

First, input variables are introduced.<p>

#### Input Variables

Input variables are variables declared in prompt template and assigned by human message during conversations.<p>

[LLMChain Version](langchain_chains/app_simple_sequential_chain_input_variables_lllmchain.py)<br>
[LCEL Version](langchain_chains/app_simple_sequential_chain_input_variables_lcel.py)<br>

#### Simple Sequential Chain

Simple sequential chain consists of only prompt and chat model.<p>
[LLMChain Version](langchain_chains/app_simple_sequential_chain_lllmchain.py)<br>
[LCEL Version](langchain_chains/app_simple_sequential_chain_lcel.py)

#### Sequential Chain
Sequential Chains can contain more than one chains. The output of a chain can be an input of the next chain.<p>

In order to apply this chain as LCEL, RunnableSequence and RunnableParallel have to be used. RunnableParallel allows us the async processing to reduce time complexity. The output variables must be declared in RunnableParallel as parameters. Then the chains were operated by RunnableSequence.<p>



![Simple Sequential Chain [7]](images/1_GkhQHtaPz1PIbLIW43vQ-A.jpg)

#### [Router Chain](router_chains)

![Router Chain [8]](images/9_yeEjVhG-thumbnail_webp-600x300.webp)

>Routing allows you to create non-deterministic chains where the output of a previous step defines the next step. Routing can help provide structure and consistency around interactions with models by allowing you to define states and use information related to those states as context to model calls.[9]<p>


Router chains allows us to use the specialized LLM. If input does not appropriate the destinations chain, the input goes to default chain.<p>

Firstly, on [the script](router_chains/app_router_chain_lllmchain.py), each prompt template of destination chains was defined. Then, dictionaries of these templates which also include name and description of destionation chains were stored in a list. Then, a dictionary was defined to include each destionation chain with names. Then, the names and descriptions of destionations were converted into string, router prompt template was declared by using MULTI_PROMPT_ROUTER_TEMPLATE. Then router promt were declared by the template and RouterOutputParser. Finally, router chain were defined by LLMRouterChain.<p>

As a result, by using MultiPromptChain, the router chain which consists of destination chains, router chain and default chain was done.


## [Document Loading and Document Splitting](langchain_doc)


# References
[1] https://python.langchain.com/docs/concepts/prompt_templates/ <br>
[2] https://python.langchain.com/api_reference/langchain/memory.html <br>
[3] https://images.app.goo.gl/sx5FcTgNzoaQKroz6 <br>
[4] https://images.app.goo.gl/wZvEEapCLpqJMw5w5 <br>
[5] https://images.app.goo.gl/TxXnsJTQhCYnSwKeA <br>
[6] https://python.langchain.com/api_reference/langchain/chains.html<br>
[7] https://images.app.goo.gl/D6J5DQMoGvMaPC3R8 <br>
[8] https://images.app.goo.gl/yThKRuJ5uTZsw9sP6 <br>
[9] https://python.langchain.com/docs/how_to/routing/<br>