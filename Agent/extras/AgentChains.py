import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from Agent.extras.agent import Agent
from langchain_classic.chains import LLMChain
from langchain_classic.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from Agent.extras.Tools import AgentTools
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.messages import HumanMessage
path = Path('/home/gz/Documents/Rebuttal AI/.env')
load_dotenv(dotenv_path=path)
api_token = os.environ['HUGGING_FACE_API_TOKEN']
templete = '''
The input is claim about a topic. Your job is to figure to what reasearch tools to call to gather infromation 
so it can be used to construct a counter argument to the claim. 
Here are the tools:
Web Search tools: this takes subject,event, or any query returns factual or live information from the web.
functiona name: search


Wiki Retriver: takes topic and returns first two or paragraph of the wikipedia that page that matches the 
topic of search.
functon name: WikiSummary

Logical fallacies: This vector db that hold list of fallacies, description and examples.
(when calling it either describe the strucutre or how claim is formed or describe the how the claim is being made and if logical fallacies matches then it will be returned)
function name: Logical_fallacies_retriver
You're output shouldn't include anything other then what is instructed below:
- output should be  in json format. keys are name of the function tools and values are queries assosiated with the fucntion call.  
- Do not add any greetings or anything else, output shoould purely what is being asked. Which is based on the claim; figure out
which functions to call and what query the funtion should get to gather information about the topics in the claim.
- Queries fo the tools are very important because that will dictate what informtion will be retrived. So create queries will get information that will be most useful to construct a 
counter argument agaisnt the claim being made.
- no more than one call per each tool.
Claim: {claim}
'''

summary_template = '''

You are researcher in a research team. You received a research information about a claim.Your job is though 
go through the information and filter out relvenet information that will be usefull building counter arguemtn.

Information is will contain content from websearch, wikipidia information, and information about logical fallacies 
the claim might have.

Your job is to use the claim and go through the research and extract relevent information and put in a
organized fashion.

output instruction:
- Ouput  should have Title called Researcha and three section: 1.Facts 2. Relevent informaton 3. Potential fallacies in 
the claim(refer to the claim made by the user and use the logical information retrived )
(Use the logical information retrived).
- cite sources if possiable.
- Organized like researchs summary academic paper. 
- nothing else should be in the output except what is instructed.

research: {info}
claim: {claim}



'''

arugment_prompt = '''
## ROLE
You are a Master Debater specializing in scientific dialectics and logical deconstruction. Your goal is to provide high-impact, evidence-based rebuttals.

## INPUT VARIABLES
- CLAIM: {claim}
- RESEARCH: {research}
- STYLE: {debate_style}

## STYLE CONTEXT & DEFINITIONS
When constructing the rebuttal, strictly follow the definition of the requested {debate_style}:
- **Academic**: Use formal syntax, peer-reviewed terminology, and a neutral, objective tone. Avoid emotional language.
- **Casual**: Use "everyday" language, relatable analogies, and a direct, conversational flow.
- **Social Media**: Use punchy, short sentences, 1-2 relevant emojis, and a clear "hook." Optimized for character limits.
- **Witty**: Use sharp metaphors, dry humor, and a skeptical or mocking edge toward the claim's logic.

## TASK
Analyze the provided claim against the research data. Identify the most critical factual inaccuracy or logical fallacy. Construct a counter-argument that adheres strictly to the {debate_style}.

## OPERATIONAL GUARDRAILS
- **No Greetings**: Do not say "Hello," "I am ready," or "Here is your rebuttal."
- **Fallacy Focus**: Name and briefly explain the specific logical fallacy present in the {claim}.
- **Evidence Limit**: Use a maximum of TWO high-impact facts from the research.
- **Brevity**: Unless a "long response" is explicitly requested in the research notes, keep the response under 150 words to ensure it is "copy-paste" ready.
- **Citations**: If the research contains specific source names, cite them in brackets, e.g., [NASA 2024].
'''

tools = AgentTools()
parser = StrOutputParser()

#llm = ChatOllama(model="gemma3:4b-it-qat", temperature=0,num_ctx=8000)
'''llm = HuggingFaceEndpoint(
    repo_id='MiniMaxAI/MiniMax-M2.1',
    task="conversational",  
    max_new_tokens=1000,
    temperature=0.7,  # Add this for better results
    huggingfacehub_api_token=api_token,
    provider="auto"
)'''
# Option 2: Use a model known to work on free tier
llm = HuggingFaceEndpoint(
    repo_id='openai/gpt-oss-120b',
    task="conversational",
    max_new_tokens=2000,
    huggingfacehub_api_token=api_token
)
chat_model = ChatHuggingFace(llm=llm)







json_parser = JsonOutputParser()
prompt_template = PromptTemplate(input_variables=["claim"],template=templete)
prompt_template_2 = PromptTemplate(input_variables=["info","claim",],template=summary_template)
argument_template = PromptTemplate(input_variables=["research","claim","debate_style"],template=arugment_prompt)
tools_selection_chain = prompt_template | chat_model| json_parser 
#claim = 'Soccer is the best sport in the world. Everyone either loves to play or watch soccer.'
#response = tools_selection_chain.invoke({'claim':claim})
#info = tools.research(response)
summary_chain = prompt_template_2 | chat_model | parser
counter_argument_chain = argument_template | chat_model | parser



st.markdown(
    f"""
    <style>
   
    .stApp {{
        background-color: #ffebcd;
    }}

   
    .stApp, .stMarkdown, p, span, label {{
        color: #4b3621 !important;
    }}

   
    h1, h2, h3 {{
        color: #2e1a0a !important;
    }}

  
    code {{
        color: #4b3621 !important;
        background-color: rgba(255, 255, 255, 0.4) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Rebuttal Ai")

# ... rest of your code
debate_style = st.radio("Style", ["Academic", "Casual", "Social Media", "Witty"], horizontal=True)
input_text = st.text_input('Write a Claim to rebuttal')
if input_text:
    with st.chat_message("assistant"):
        # 1. Run Logic
        tools_calls = tools_selection_chain.invoke({'claim': input_text})
        info = tools.research(tools_calls)
        summary = summary_chain.invoke({"info": info, "claim": input_text})
        
        rebuttal = counter_argument_chain.invoke({
            'research': summary, 
            'debate_style': debate_style, 
            'claim': input_text
        })
        
        # 2. Display Rebuttal in a Code block for the "Copy" icon
        # 'language=None' keeps it looking like clean text
        st.write(rebuttal)
        
        # 3. Research comes after
        with st.expander("🔍 View Research Data"):
            st.write(summary)
            st.write(tools_calls)
