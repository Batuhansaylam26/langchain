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


Document loading and splitting are fundamental steps for processing large documents and enabling more efficient querying. LangChain allows you to load documents from various sources and split these documents into smaller chunks, making LLMs work more effectively.<p>

![doc loading scheme [11]](images/doc.png)


### [Document Loader](langchain_doc/app_doc_load.py)

First, documents are loaded in different formats (txt, pdf, docx, etc.). In the script, the appropriate loader class (PyPDFLoader) from langchain.document_loaders is selected, the file path is specified, and the documents are loaded. The loader returns the document content as a list. In this list, the pages were stored. Also, the pages content between first and 50th characters are displayed.<p>


### Document Splitter

Since loaded documents are often very large, they are split into smaller chunks to help LLMs understand them better. In the script, LangChain's splitter functions are used to divide documents based on a specific word or character count. Each chunk can be processed as a separate document.<p>

There are many types of splitter. There several of them are:
* CharacterTextSplitter
* CodeTextSplitter
* MarkdownHeaderTextSplitter
* RecursiveCharacterSplitter
* TokenTextSplitter
<p>
All of them need a list of pages to split into chunks in order to recognize the some characters such as "\n\n", "\n", " ", "".<p> 

Futhermore, the loading and splitting steps are combined into a pipeline. The document is first loaded, then split into chunks, and if necessary, prepared for embedding or retrieval. This enables faster and more efficient search, summarization, or question-answering operations on documents.<p>

With these scripts, you can easily manage the data preparation process when developing document-based applications with LangChain.<p>

#### [Character Text Splitter](langchain_doc/app_CharachterTextSplitter.py)

CharacterTextSplitter is one of the basic text splitting tools in LangChain. It splits documents into smaller chunks based on a specified character, such as a space or newline. This helps large documents become manageable for language models.<p>

In the script, after loading the text file (txt) using the open function, the CharacterTextSplitter class is initialized. For initialization, the chunk size is set to 200 and the chunk overlap is set to 20.<p>

Chunk overlap helps preserve context between chunks, ensuring that important information is not lost at the boundaries.<p>


#### [Recursive Character Splitter](langchain_doc/app_RecursiveCharachterTextSplitter.py)

In some cases, documents need to be split in a more sophisticated way. With RecursiveCharacterTextSplitter, documents are split by paying attention to sentence or paragraph boundaries. This method reduces information loss and helps obtain more meaningful chunks.<p>

> This text splitter is the recommended one for generic text. It is parameterized by a list of characters. It tries to split on them in order until the chunks are small enough. The default list is ["\n\n", "\n", " ", ""]. [10] <p>

On the script, after the text file (txt) was loaded by using open, the class of the splitter was initialized. For the initialization, the chunk size was defined as 20 and chunk overlap was defined as 3.<p>

The chunk overlap allows us to avoid losing the context information for each chunk.<p>

## [Embeddings and Vectorstore](langchain_vectorStore_embeddings)

![RAG [12]](images/1_8eLGJBNzL9TQBkrgBOiBfw.png)


Embeddings are vector representations of text that capture semantic meaning, enabling advanced search and retrieval capabilities. Vectorstores are specialized databases designed to store and efficiently search these embeddings.

In this section, various scripts demonstrate how to generate embeddings using Google Generative AI, store them in a vector database (ChromaDB), and perform semantic similarity searches and retrieval-augmented question answering.

- **Embeddings and Semantic Similarity:** Texts are converted into embeddings, and their semantic similarity is calculated using vector operations. This allows for meaningful comparison beyond simple keyword matching.
- **Saving Embeddings and Similarity Search:** Documents (such as PDFs) are loaded, split into chunks, embedded, and stored in a persistent vectorstore. Queries can then be run to find the most relevant document chunks based on semantic similarity.
- **Retriever and Retrieval QA Chain:** A retriever is built from the vectorstore to enable semantic search. A RetrievalQA chain uses the retriever and a language model to answer questions based on the retrieved context, also providing source citations.

These workflows enable scalable, efficient, and context-aware search and question answering over large collections of unstructured documents using LangChain and modern embedding models.

### [Embeddings and Semantic Similarity](langchain_vectorStore_embeddings/app_embeddings_semantic_similarity.py)

Semantic similarity is a technique used to measure how similar two pieces of text are in meaning, rather than just in wording. In this script, Google Generative AI's embedding model is used to generate vector representations for different texts.<p>

First, the environment variables are loaded and the Gemini model is initialized for both chat and embedding tasks. Three sample texts are defined: "Kitty", "Rock", and "Cat". Each text is converted into an embedding vector using the GoogleGenerativeAIEmbeddings class.<p>

To calculate the semantic similarity between two texts, the dot product of their embedding vectors is computed using NumPy. A higher similarity score indicates that the texts are more closely related in meaning.<p>

This approach allows you to compare the semantic content of different texts, which is useful for tasks such as search, clustering, and recommendation in NLP applications.<p>

### [Saving Embeddings and Similarity Search](langchain_vectorStore_embeddings/app_saving_embeddings_similarity_search.py)

This script demonstrates how to load a PDF document, split it into manageable chunks, generate embeddings for each chunk, and store them in a persistent vector database for efficient similarity search.

First, the document is loaded using PyPDFLoader. The RecursiveCharacterTextSplitter is used to divide the document into chunks of 2000 characters with an overlap of 150 characters, ensuring that context is preserved between chunks.

The GoogleGenerativeAIEmbeddings model is used to generate vector representations for each chunk. These embeddings are then stored in a Chroma vector database, which is created in a specified directory for persistence.

To perform a similarity search, a query such as "What is Batuhan's education?" is provided. The vector database retrieves the most relevant chunks based on semantic similarity to the query. The top results are printed, allowing you to quickly find information within large documents.

This workflow enables scalable and efficient document search, making it easy to retrieve relevant information from unstructured data using LangChain and vector databases.

### [Retriever and Retrieval QA Chain](langchain_vectorStore_embeddings/app_retrievers.py)

This script demonstrates how to build a document retriever and a question-answering chain using LangChain and Google Generative AI embeddings.<p>

First, a PDF document is loaded and split into manageable chunks using RecursiveCharacterTextSplitter. Each chunk is embedded with GoogleGenerativeAIEmbeddings and stored in a Chroma vector database. The database is persisted for later use.<p>

A retriever is created from the vector store (ChromaDB), allowing semantic search over the document chunks. When a query such as "Tell me more about Batuhan SAYLAM" is provided, the retriever returns the most relevant chunks.<p>

To answer questions based on the retrieved documents, a RetrievalQA chain is constructed using the Gemini chat model. The chain takes the retriever as input and generates answers using the retrieved context. The script also includes a helper function to display the answer and cite the sources from which the information was retrieved.<p>

This workflow enables efficient, source-aware question answering over large documents, combining semantic search and generative AI for robust retrieval-augmented generation.<p>

## [Agents](langchain_agents)
>LangChain supports the creation of agents, or systems that use LLMs as reasoning engines to determine which actions to take and the inputs necessary to perform the action. After executing actions, the results can be fed back into the LLM to determine whether more actions are needed, or whether it is okay to finish. This is often achieved via tool-calling. [13]<p>

![agent [14]](images/1_PQHNtQQkq1ga0Sdh3Uui8w.png)

This approach allows you to extend your agent's capabilities by adding specialized tools for different tasks, such as math, search, or code execution.<p>


**Some Agent Types**

LangChain supports several agent types, each designed for different use cases:

- **Zero-Shot-React-Description:**  
  This agent uses a language model to decide which tool to use for each query, without requiring explicit examples. It reacts to the user's input and selects the appropriate tool based on the tool descriptions.<p> Also, it needs one single interaction with agent -it will have no memory.<p>

- **Conversational-React-Description:**  
  This agent extends the zero-shot-react approach by maintaining conversation history. It uses memory to keep track of previous interactions, enabling context-aware responses and more natural conversations.<p>

- **React-Docstore:**  
  This agent is specialized for interacting with document stores. It can search, retrieve, and answer questions based on documents, making it useful for knowledge base and retrieval-augmented tasks.<p> It has been built for information search and look up using langchain docstore.

Each agent type can be configured with different tools and memory options to suit specific workflows, such as math reasoning, general knowledge, web search, or document retrieval.

### [LLM Math Chain Tool](langchain_agents/app_llmathchain_tool.py)

This script demonstrates how to create a math tool agent using LangChain and Google Generative AI. The LLMMathChain enables the language model to perform mathematical calculations and answer math-related questions.<p>

First, the Gemini model is initialized for chat-based interactions. The LLMMathChain is wrapped in a Tool object, named "Calculator", with a description indicating its purpose. This tool can be integrated into agent workflows, allowing the agent to handle queries that require mathematical reasoning or computation.<p>

The script prints the name and description of the tool, confirming its setup.<br>

### [Math Agent](langchain_agents/app_buitin_math_tool_testing_agent.py)

This script shows how to create an agent in LangChain that can perform mathematical reasoning using Google Generative AI. The Gemini model is initialized for chat interactions. The agent is equipped with the LLMMathChain tool by using load_tools, allowing it to answer math-related queries.<p>

The agent uses a single chat model instance for both decision-making and tool execution. The agent selects the appropriate tool, and the chat model processes the prompt and provides the response.<p>

The agent is set up with a maximum of 3 iterations to control costs. When invoked with a math question (e.g., `"What is 3.1**2.1"`), it uses the calculator tool to compute the answer. For factual questions outside its toolset (e.g., `"What is the capital of Mozambique"`), the agent responds that it cannot answer, demonstrating tool-based limitations.<p>

This approach enables agents to handle specialized tasks by integrating tools, and clearly shows how tool-calling restricts the agent’s capabilities to its configured tools.<p>

Example output:<br>
```
> Entering new AgentExecutor chain...
I don't have the tools to answer factual questions about geography. I am an AI assistant that can only use the calculator tool.
Final Answer: I am sorry, I cannot answer this question.

> Finished chain.
I am sorry, I cannot answer this question.
```



### [General Knowledge & Math Agent](langchain_agents/app_general_knowledge_tool.py)

This script demonstrates how to create an agent in LangChain that can answer both general knowledge and math questions using Google Generative AI. The Gemini model is initialized for chat interactions. Two tools are added to the agent:<p>
- **LLMMathChain** for mathematical reasoning by loading load_tools.
- **LLMChain** for general queries and logic.

The agent is set up with a maximum of 3 iterations. When invoked with a factual question (e.g., `"What is the capital of China?"`), it uses the general knowledge tool. For math-related queries (e.g., age or arithmetic calculations), it uses the calculator tool.<p>

This approach enables agents to handle a wider range of tasks by integrating multiple specialized tools.<br>

Example output:<br>
```
> Entering new AgentExecutor chain...
Observation: The capital of China is Beijing.
Final Answer: Beijing

> Finished chain.
Beijing
```

### [Conversational Agent with Memory](langchain_agents/app_conversational_agents_memory.py)

This script shows how to build a conversational agent in LangChain that can answer both general knowledge and math questions, while maintaining conversation history using memory. The Gemini model is initialized for chat interactions. The agent uses two tools:
- **LLMMathChain** for mathematical reasoning.
- **LLMChain** for general queries and logic.

A `ConversationBufferMemory` object is added to the agent, enabling it to remember previous exchanges and use context from earlier questions. This allows for more natural, context-aware conversations.

Example output:
```
> Entering new AgentExecutor chain...
Observation: James will be 95 years old in 50 years. He has 11 children in total.
Final Answer: James will be 95 years old in 50 years and has 11 children.

> Finished chain.
James will be 95 years old in 50 years and has 11 children.

> Entering new AgentExecutor chain...
Observation: If James had only 3 kids, he would have 10 children in total (3 + 7 adopted).
Final Answer: If James had only 3 kids, he would have 10 children in total.

> Finished chain.
If James had only 3 kids, he would have 10 children in total.
```
### [Wikipedia Agent](langchain_agents/app_agent_wikipedia.py)

This script shows how to create an agent in LangChain that can answer factual questions using Wikipedia as a search tool. The Gemini model is initialized for chat interactions. The agent uses the `WikipediaQueryRun` tool, which queries Wikipedia and returns the most relevant result.

The agent is set up with a maximum of 5 iterations to handle complex queries. When invoked with a question (e.g., `"What was Bach's last piece he wrote?"`), it searches Wikipedia and provides a concise answer.

Example output:
```
--- Nihai Cevap ---
Bach's last piece was the chorale prelude "Vor deinen Thron tret' ich hiermit" (Before Thy Throne I Now Appear), BWV 668.
```

### [Self-Ask Agent with Google Search](langchain_agents/app_self_ask_agent.py)

This script demonstrates how to create a LangChain agent that can answer complex questions by decomposing them into sub-questions and using Google Search (via SerpAPI) for intermediate answers. The Gemini model is initialized for chat interactions. The agent uses the `self-ask-with-search` agent type and a search tool powered by SerpAPI.

When invoked with a question (e.g., `"How to bake a cake with 123 ingredients?"`), the agent breaks down the query, searches for relevant information, and provides a detailed answer.

Example output:
```
--- Nihai Cevap ---
To bake a cake with 123 ingredients, you would need to carefully organize and measure each ingredient, follow a comprehensive recipe, and ensure proper mixing and baking techniques. (Example answer, actual output may vary based on search results.)
```


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
[10] https://python.langchain.com/docs/how_to/recursive_text_splitter/ <br>
[11] https://images.app.goo.gl/F6HuicyQAVrDN3Pb7 <br>
[12] https://images.app.goo.gl/PHBXuUJ9KE7ntAJDA <br>
[13] https://python.langchain.com/docs/tutorials/agents/ <br>
[14] https://images.app.goo.gl/8xqFHVfyE7ikM4ir5 <br>