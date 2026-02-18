import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from LLM_Tools import search,wiki_summary,logical_fallacies_retriever,get_json
from prompts import research_system_prompt,web_search_agent_prompt,quick_response_system_prompt,follow_up_system_instructions
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_community.llms.fake import FakeListLLM
from langchain_core.output_parsers import JsonOutputParser
import time
path = Path('/home/gz/Documents/Rebuttal AI/.env')
load_dotenv(dotenv_path=path)
api_token = os.environ['HUGGING_FACE_API_TOKEN']
# 'openai/gpt-oss-120b'
class Agent:

    def __init__(self):
        '''self.hf_model = HuggingFaceEndpoint(
                    repo_id='openai/gpt-oss-120b',
                    task="conversational",
                    max_new_tokens=2000,
                    huggingfacehub_api_token=api_token
                )'''
        
        #self.llm = ChatOllama(model='qwen3:8b', temperature=0,num_ctx=4100)
        self.parser = JsonOutputParser()

        
        #ChatHuggingFace(llm=self.hf_model)
        '''self.research_Agent = create_agent(
            model=self.llm,
            tools=[search,logical_fallacies_retriever,wiki_summary,get_json],
            system_prompt=research_system_prompt,
            

        )
        self.web_search_agent = create_agent(
            model=self.llm,
            tools=[search], 
            system_prompt=web_search_agent_prompt

        ) '''
    
    
    def debug_get_agent_response(self, inputs,agent):  
        prompt= {
        "messages": [{"role": "user", "content": inputs}]
        }
    
        
       
        for chunk in agent.stream(
            prompt,
            
        ):
            print("\n" + "="*50)
            print("STEP:")
            print("="*50)
            print(chunk)
            print()
        
        # Last chunk IS the final result
        final_result = chunk
        
        # Print final answer
        print("\n" + "="*50)
        print("FINAL ANSWER:")
        print("="*50)
        print(final_result)
    def research_agent_response(self, claim):
        prompt= {
        "messages": [{"role": "user", "content": claim}]
        }
    
        result = self.research_Agent.invoke(prompt)
        response = result["messages"][-1].content
        return self.parser.parse(response)
        
        
        
    def websearch_agent_response(self,claim):
        prompt= {
        "messages": [{"role": "user", "content": claim}]
        }
        result = self.web_search_agent.invoke(prompt)
        
        
        response = result["messages"][-1].content

        return self.parser.parse(response)
    
    def fast_agent_response(self,claim):
        messages = [
        (
            "system",
            quick_response_system_prompt,
        ),
        ("human", claim),]
        result =self.llm.invoke(messages)
        return self.parser.parse(result.content)
        
    def follow_up(self,history,question):
        prompt = f'History: {history}, \n query: {question}'
        messages = [
        (
            "system",
            follow_up_system_instructions,
        ),
        ("human", prompt),]
        result = self.llm.invoke(messages)
        return result.content
    def MockLLMCall(self,claim):
        fake_json2 = {
            "response": "Recent studies indicate that human-driven deforestation and fossil fuel use are major factors accelerating climate change worldwide.",
            "details": {
                "title": "Drivers of Modern Climate Change",
                "authors": ["Maria Gonzalez", "Li Wei"],
                "year": 2021,
                "citations": 98,
                "url": "https://doi.org/fake2"
            }
        }
        fake_json = {
            "response": "Human activities, particularly the emission of greenhouse gases, have significantly contributed to global climate change over the past century.",
            "details": {
                "title": "Human Impact on Climate Change",
                "authors": ["Jane Smith", "Alan Doe"],
                "year": 2022,
                "citations": 134,
                "url": "https://doi.org/fake1"
            }
        }
        time.sleep(8)
        return fake_json2


        

user_input = f"""
                  Claim:
                    Water boils at 100°C at sea level, so you don’t need a thermometer to know when it’s boiling.

                    Requested style:
                    Social Media

                    Requested length:
                    short

                    """



'''
agent = Agent()
#agent.debug_get_agent_response(user_input,agent.research_Agent)


res = agent.research_agent_response(claim=user_input)
print(res)
print(res['details'])
print(res[
    'counter_argument'])
'''