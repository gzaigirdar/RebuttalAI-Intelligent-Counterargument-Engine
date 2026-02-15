import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from Agent.extras.agent import Agent
system_template = """You are a master debater. 
Do not greet the user. Do not say "I am ready." 
Focus on scientific facts and logical fallacies.
Treat this as you are debating user.
Be precise and concise.
Don't use more than two supporting evidence.
Keep it brief so the rebuttal can be copied and paste it social media or private messages,unless instructed for a long response.
here are the tools:
    Wikipedia function: takes a topic and then returns first few paragraphs of the  first page of the matched topic.
    

    search function:
    searches web for factual information,current events, stats, and other things.
    Utilize these tools to proive storng counter arguement     
   



    Logical_fallacies_retriver function:
    retrives documents about logical fallacies from vector db
    don't be hestiant to look up facts using search and make source cite your sources.
    -  search 
"""



agent = Agent(system_prompt=system_template)
output_parser = StrOutputParser()

st.title("Simple agent ai with Ollama")
input_text = st.text_input('Write a Claim to rebuttal')

if input_text:
    response = agent.ask(input_text)
    st.write(output_parser.parse(response))
