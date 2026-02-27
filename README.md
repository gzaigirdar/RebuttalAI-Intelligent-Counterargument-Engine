## Rebuttal AI – Agentic Counterargument System

Rebuttal AI is an agentic AI system designed to autonomously generate fact driven counterarguments to user provided statements or claims. Using integrated tools such as web search, Wikipedia summaries, and a logical fallacies knowledge base. Rebuttal AI analyzes claims and produces structured, evidence backed rebuttals without requiring any additional instructions from the user.

### Demo App is deployed in streamlit  cloud:
[App link](https://refuteai.streamlit.app/)

User Interaction:
Users interact with Rebuttal AI in a simple, intuitive way by prroviding a claim or statement.
Use can customize their coutner to their liking by selecting  preferences such as Style (academic, social media, casual, witty)Response length(short, medium, long) and Agent type(web agent, research agent, fast agent)
Follow up conversations are supported for users who want more information, clarification, or wish to engage in a discussion regarding the claim and counterargument.

System Architecture:
Rebuttal AI uses multiple agents that wre built with LangChain and LangGraph, integrating agents, tools, and utility functions.
there agents were created such as Web Agent(response with web seearch tool), Research Agent(deep researched based), Fast Agent(quick response without tools), each with diffirent prompt and purposes. (LLM_Agents.Py)

Frontend was developed with Streamlit and custom CSS for a user friendly, visually polished interface.(App.py,SidebarUI.py,ChatUi.py)

Prompts were carefully curated to maximize reasoning and response quality for smaller models, covering different agent types and follow up behaviors. There sytem prompts are Research Prompts, Web Agent Prompts, Fast Agent Prompts, Follow-up Prompts.(prompts.py)

The three integrated tools are DuckDuckGo Search API,Wikipedia Summary API,Logical Fallacies Vector DB(built using FAISS, storing definitions and examples of common logical fallacies to detect flaws in claims.) (LLM_Tools.py,create&save_vector_store.ipynb.)

Rebuttal AI is designed to work with smaller, efficient models, optimizing performance without requiring extremely large LLMs.
so local Ollama Models(Qwen:8b), and hugging face models were used during development.Groq models were used for perfomance testing and delployment.

How to run the app:
## Create virtual environment
python -m venv venv

## Install dependencies
pip3 install -r requirements.txt

## Select backend (Ollama, Hugging Face, Groq)
 Modify LLM_Agent.py accordingly

## Run the app
streamlit run App.py


