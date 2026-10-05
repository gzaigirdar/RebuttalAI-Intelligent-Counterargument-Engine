# Rebuttal AI – Agentic Counterargument System

Rebuttal AI is an agentic AI system designed to autonomously generate fact-driven counterarguments to user-provided statements and claims.

The system uses multiple specialized agents together with external tools such as web search, Wikipedia retrieval, and a FAISS-based logical fallacy knowledge base. Based on the selected agent mode, Rebuttal AI can generate a quick response, gather current information from the web, or perform a deeper evidence-based analysis.

The application also supports follow-up conversations, allowing users to ask for clarification, additional evidence, or continue discussing the original claim.

## Live Application

Rebuttal AI is deployed on an Oracle Cloud VPS:

[https://rebuttalai.online/](https://rebuttalai.online/)

## Features

Users provide a claim or statement and can customize the generated counterargument using:

- **Agent Type**
  - Fast Agent
  - Web Agent
  - Research Agent

- **Response Style**
  - Academic
  - Casual
  - Social Media
  - Witty

- **Response Length**
  - Short
  - Medium
  - Long

- **Follow-up Conversation**
  - Ask for clarification
  - Request additional evidence
  - Continue discussing the original argument
  - Maintain recent conversation context

## Agent Architecture

Rebuttal AI uses multiple specialized agents built with LangChain and LangGraph.

### Fast Agent

Generates quick counterarguments without calling external retrieval tools. This mode is intended for claims that can be addressed directly by the language model.

### Web Agent

Uses web search and Wikipedia retrieval to gather additional information before generating a counterargument.

### Research Agent

Performs a more detailed analysis using retrieval tools and external evidence. This mode is designed for claims that require deeper research and reasoning.

Each agent uses its own system prompt and workflow based on its specific purpose.

Agent implementation:

`LLM_Agents.py`

## Retrieval and Tools

Rebuttal AI integrates three primary tools:

### DuckDuckGo Search

Provides web search capabilities for retrieving current information related to a user's claim.

### Wikipedia Retrieval

Retrieves concise background information and summaries for relevant topics.

### Logical Fallacies Vector Database

A FAISS vector database stores definitions and examples of common logical fallacies.

Relevant information is retrieved through semantic similarity, allowing the system to identify reasoning patterns that may be present in a user's claim.

Tool implementation:

`LLM_Tools.py`

Vector database creation:

`create&save_vector_store.ipynb`

## Prompt Engineering

Different system prompts were created for each agent and interaction type:

- Research Agent Prompt
- Web Agent Prompt
- Fast Agent Prompt
- Follow-up Prompt

The prompts define how agents analyze claims, use retrieved information, structure responses, and follow the user's selected response style.

Prompt definitions:

`prompts.py`

## Models and Inference

Rebuttal AI was designed to work with multiple model providers and model sizes.

During development, the system was tested with:

- Local Ollama models such as Qwen
- Hugging Face models
- DeepInfra-hosted models

The current agent configuration uses:

- **GPT-OSS-120B** for the Fast and Web agents
- **DeepSeek Flash V1** for the Research agent
- **Qwen embedding model through Ollama** for semantic retrieval

This architecture allows different models to be assigned to different agents based on response speed, reasoning requirements, and task complexity.

## Frontend

The user interface was developed with Streamlit and custom CSS.

The interface provides:

- Interactive chat
- Agent selection
- Response style selection
- Response length controls
- Follow-up conversations
- Display of generated counterarguments and supporting information

Frontend components include:

- `App.py`
- `SidebarUI.py`
- `ChatUi.py`

## Deployment

The production application is deployed on an Ubuntu-based Oracle Cloud VPS.

The deployment architecture is:

User → HTTPS → Nginx → Streamlit

The Streamlit application runs internally on:

`127.0.0.1:8501`

and is not directly exposed to the public internet.

Nginx is used as a reverse proxy between the public website and the Streamlit backend.

The deployment includes:

- Oracle Cloud VPS
- Dockerized Streamlit application
- Nginx reverse proxy
- WebSocket proxy support
- Custom domain configuration
- OCI network security rules
- UFW firewall configuration
- Per-IP request rate limiting
- Per-IP connection limiting
- Separate static asset rate limiting
- HTTPS using Let's Encrypt
- Automatic TLS certificate renewal with Certbot

The application is available at:

[https://rebuttalai.online/](https://rebuttalai.online/)

## Security and Reliability

Several protections were added to the production deployment:

- Streamlit is restricted to localhost and cannot be accessed directly from the internet.
- Nginx acts as the public-facing reverse proxy.
- OCI and UFW firewall rules restrict exposed ports.
- Per-IP request limits help reduce excessive traffic.
- Concurrent connection limits reduce abusive connection usage.
- Static resources use separate rate limits to prevent normal Streamlit page loading from being blocked.
- HTTPS encrypts communication between users and the server.
- Let's Encrypt certificates are automatically renewed using Certbot.

Nginx access and error logs were also used to diagnose and resolve production issues including `502 Bad Gateway` and `503 Service Temporarily Unavailable` errors.

## Project Structure

```text
RebuttalAI/
│
├── Agent/
│   ├── App.py
│   ├── LLM_Agents.py
│   ├── LLM_Tools.py
│   ├── prompts.py
│   ├── SidebarUI.py
│   ├── ChatUi.py
│   └── Logical_Fallacies_DB/
│
├── create&save_vector_store.ipynb
├── requirements.txt
└── README.md