from langchain_core.tools import tool
from langchain_classic.agents import create_react_agent, AgentExecutor, create_tool_calling_agent
from langchain_classic.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain_core.prompts import PromptTemplate  # ← ADD THIS
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.retrievers import WikipediaRetriever
from langchain_ollama import ChatOllama
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
# Initialize Ollama model
llm = ChatOllama(model="qwen3:4bz", temperature=0,num_ctx=10000)
#llm = OllamaLLM(model='gemma3:4b', num_ctx=5000, num_predict=1000)
# Initialize tools
search_tool = DuckDuckGoSearchRun()
wiki_retriever = WikipediaRetriever()
memory = ConversationBufferWindowMemory(memory_key='chat_history',return_messages=True)

parser = StrOutputParser()
@tool
def search(query: str) -> str:
    """Search the web for live facts, events, news, and other information."""
    return search_tool.run(query)


@tool
def WikiSummary(query: str, num_chars: int = 1500) -> str:
    """Get a Wikipedia summary for a topic/event/person."""
    # CHANGED: Use .invoke(query) instead of ._get_relevant_documents(query)
    docs = wiki_retriever.invoke(query) 
    if not docs:
        return "No results found."
    return docs[0].page_content[:num_chars]

tools = [search, WikiSummary]

# FIXED: Create PromptTemplate object
system_msg = """

You are a master debater. 
Do not greet the user. Do not say "I am ready." 
Focus on scientific facts and logical fallacies.
Treat this as you are debating user.
Be precise and concise.
Don't use more than two supporting evidence.
Keep it brief so the rebuttal can be copied and paste it social media or privatfor a long response.e messages,unless instructed.
Use a mocking or skeptical tone toward logical fallacies. 
here are the tools:
WikiSummary function that returns first page of the topic you search

search function:
searches web for factual information,current events, stats, and other things.
Utilize these tools to proive storng counter arguement                              

                                        
"""

from langchain_core.prompts import ChatPromptTemplate

# 1. Use a Chat-specific prompt (Tool calling works best with Chat templates)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_msg),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 2. Initialize the modern Tool Calling Agent
# This tells the LLM: "Here is the schema for my search and wiki tools."
agent = create_tool_calling_agent(llm, tools, prompt)

# 3. Create the Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory # Your existing memory object
)

# 4. Run it
# If you say "Hi", it will just reply. 
# If you say "Who won the soccer match today?", it will call the tool.
response = agent_executor.invoke({"input": "Soccer is the Best sport in the world. Everyone loves either to watch or play soccer"})
print(parser.parse(response['output']))














'''

# Create agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

# Test
response = agent_executor.invoke({"input": "Soccer is the besst sport in the world,Everyone loves soccer."})
print(response['output'])
'''