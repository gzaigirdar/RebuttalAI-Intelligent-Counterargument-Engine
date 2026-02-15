from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.retrievers import WikipediaRetriever
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

class Agent:
    def __init__(self, system_prompt):
        # Tools
        search_tool = DuckDuckGoSearchRun()
        wiki_retriever = WikipediaRetriever()
        
        @tool
        def search(query: str) -> str:
            """Search the web for live facts, events, news."""
            return search_tool.run(query)
        
        @tool
        def WikiSummary(query: str, num_chars: int = 3000) -> str:
            """Get Wikipedia summary for topic/person."""
            docs = wiki_retriever.get_relevant_documents(query)
            return docs[0].page_content[:num_chars] if docs else "No results."
        
        self.tools = [search, WikiSummary]
        
        # Memory
        self.Memory = ConversationBufferWindowMemory(
            k=2, memory_key='chat_history', return_messages=True
        )
        
        # Ollama
        self.LLM = ChatOllama(model='qwen3:4b', temperature=0)
        
        # Conversational prompt WITH tools
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt + "\n\nYou have tools available. Use them when you need facts/data. Respond naturally."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Tool-calling agent (no ReAct format needed)
        self.agent = create_tool_calling_agent(
            llm=self.LLM,
            tools=self.tools,
            prompt=self.prompt
        )
        
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=2
        )
    
    def invoke(self, input_dict):
        return self.executor.invoke({"input": input_dict["input"]})

# Debate agent
system_template = """You are a master debater. 
Do not greet. Focus on scientific facts and logical fallacies.
Treat this as debate. Be precise, concise. Max 2 supporting facts.
Keep brief for social media."""

agent = Agent(system_template)
response = agent.invoke({"input": "Soccer is the best sports in the wrold.Everybody loves to watch and play soccer."})
print(response['output'])
