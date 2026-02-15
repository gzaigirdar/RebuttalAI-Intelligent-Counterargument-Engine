from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
# Ensure your Tools.py is in the same directory
from Agent.extras.Tools import AgentTools

class Agent:
    def __init__(self):
        # 1. Initialize Tools
        tools_provider = AgentTools()
        self.tools = [
            tools_provider.search, 
            tools_provider.Wiki_Summary, 
            tools_provider.Logical_fallacies_retriver
        ]

        # 2. Setup LLM (Ministral via Ollama)
        self.llm = ChatOllama(model="ministral-3:8b", temperature=0)

        # 3. System Instructions (The "Master Debater" Persona)
        system_instructions = """
            You are a master debater. 
            Do not greet the user. Do not say "I am ready." 
            Focus on scientific facts and logical fallacies.
            Treat this as you are debating the user.
            Be precise and concise.
            Don't use more than two supporting evidence.
            Keep it brief so the rebuttal can be copied and pasted easily.
            Use a mocking or skeptical tone toward logical fallacies.
        """

        # 4. Persistence (Memory)
        # MemorySaver allows the agent to remember the thread history
        self.memory = MemorySaver()

        # 5. Build the Agent Graph
        # Using 'prompt' as the keyword for the system message
        self.app = create_react_agent(
            self.llm,
            tools=self.tools,
            checkpointer=self.memory,
            prompt=system_instructions
        )

        # Thread configuration (keep this ID the same to maintain a conversation)
        self.config = {"configurable": {"thread_id": "debate_001"}}

    def ask(self, query: str):
        """
        Sends the query to the graph and returns the final string response.
        """
        # Prepare input in the expected message format
        inputs = {"messages": [HumanMessage(content=query)]}
        
        # Run the graph
        result = self.app.invoke(inputs, config=self.config)
        
        # result["messages"] contains the full history of this turn
        # The final index is the AI's last response
        return result["messages"][-1].content

# --- Execution Block ---
if __name__ == "__main__":
    debater = Agent()
    claim = 'Soccer is the best sport in the world. everyone loves to play soccer.'
    rebuttal = debater.ask(claim)
    print(f"\nDebater: {rebuttal}\n")

    
    '''
    print("--- DEBATER READY ---")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        rebuttal = debater.ask(user_input)
        print(f"\nDebater: {rebuttal}\n")
    '''