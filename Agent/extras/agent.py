from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.agents import create_react_agent, AgentExecutor,create_tool_calling_agent
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from Tools import AgentTools
from langchain_ollama import ChatOllama
from prompts import research_system_prompt

class Agent:

    def __init__(self,system_prompt):

        Tool = AgentTools()
        self.tools = [Tool.search, Tool.Wiki_Summary, Tool.Logical_fallacies_retriver]

        # Build the system prompt with tools info
      

      
                                                            
                        

        self.Prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])


        self.Memory = ConversationBufferWindowMemory(k=2, memory_key='chat_history', return_messages=True, input_key='input')
        self.parser = StrOutputParser()
        self.LLM = ChatOllama(model="ministral-3:8b", temperature=0,num_ctx=10000)

        self.Agent = create_tool_calling_agent(
            llm=self.LLM,
            tools=self.tools,
            prompt=self.Prompt_template,
        )

        self.Agent_executor = AgentExecutor(
            agent=self.Agent,
            tools=self.tools,
            memory=self.Memory,
            verbose=True,
            handle_parsing_errors=True
        )

    def ask(self, query, style="Casual", length="short"):
        user_input = f"""
                    Claim:
                    {query}

                    Requested style:
                    {style}

                    Requested length:
                    {length}
                    """
        response = self.Agent_executor.invoke({"input": user_input})
        return response["output"]


agent = Agent(system_prompt=research_system_prompt)

print(
    agent.ask(
        query="Climate change is mostly caused by natural cycles rather than human activity, so aggressive emissions policies are unnecessary.",
        style="Casual",
        length="short"
    )
)


    




