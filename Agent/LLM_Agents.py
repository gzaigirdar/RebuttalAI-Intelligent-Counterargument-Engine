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
from langchain_groq import ChatGroq;
import time
path = Path('/home/gz/Documents/Rebuttal AI/.env')
load_dotenv(dotenv_path=path)
api_token = os.environ['GROQ_API_TOKEN']
# 'openai/gpt-oss-120b'
class Agent:

    def __init__(self):
        '''self.hf_model = HuggingFaceEndpoint(
                    repo_id='openai/gpt-oss-20b',
                    task="conversational",
                    max_new_tokens=2000,
                    huggingfacehub_api_token=api_token
                )'''
        
        #self.llm = ChatOllama(model='qwen3:8b', temperature=0,num_ctx=5000)
        self.llm = ChatGroq(
                   api_key=api_token,
                   model='openai/gpt-oss-20b',
                   max_tokens=5000
        )
        self.parser = JsonOutputParser()
        

        
        #ChatHuggingFace(llm=self.hf_model)
        self.research_Agent = create_agent(
            model=self.llm,
            tools=[search,logical_fallacies_retriever,wiki_summary],
            system_prompt=research_system_prompt,
            

        )
        self.web_search_agent = create_agent(
            model=self.llm,
            tools=[search], 
            system_prompt=web_search_agent_prompt

        ) 
    
    
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
        tool_calls = result.get("tool_calls", [])
        print(tool_calls)
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
            "response": ''' Computer science is the study of computation, information, and automation.[1][2][3] Included broadly in the sciences, 
            computer science spans theoretical disciplines (such as algorithms, theory of computation, and information theory) to applied disciplines 
            (including the design and implementation of hardware and software).[4][5][6] An expert in the field is known as a computer scientist.
            Algorithms and data structures are central to computer science.[7] The theory of computation concerns abstract models of computation and general 
            classes of problems that can be solved using them. The fields of cryptography and computer security involve studying the means 
            for secure communication and preventing security vulnerabilities. Computer graphics and computational geometry address the generation of images.
              Programming language theory considers different ways to describe computational processes, and database theory concerns the manage
            ment of repositories of data. Human–computer interaction investigates the interfaces through which humans and computers interact, and 
            software engineering focuses on the design and principles behind developing software. Areas such as operating systems, networks and 
            embedded systems investigate the principles and design behind complex systems. Computer architecture describes the construction of computer components and 
            computer-operated equipment. Artificial intelligence and machine learning aim to synthesize goal-orientated processes such as problem-solving, decision-making, 
            environmental adaptation, planning and learning found in humans and animals. Within artificial intelligence, computer vision aims to understand and process 
            image and video data, while natural language processing aims to understand and process textual and linguistic data.
            The fundamental concern of computer science is determining what can and cannot be automated.[2][8][3][9][10] The Turing Award is generally recognized as 
            the highest distinction in computer science.[11][12]''',
            
            
            "details": {
                "title": "Drivers of Modern Climate Change",
                "authors": ["Maria Gonzalez", "Li Wei"],
                "year": 2021,
                "citations": 98,
                "url": "https://doi.org/fake2"
            }
        }
        fake_json = {
            "response": ''' Computer science is the study of computation, information, and automation.[1][2][3] Included broadly in the sciences, 
            computer science spans theoretical disciplines (such as algorithms, theory of computation, and information theory) to applied disciplines 
            (including the design and implementation of hardware and software).[4][5][6] An expert in the field is known as a computer scientist.
            Algorithms and data structures are central to computer science.[7] The theory of computation concerns abstract models of computation and general 
            classes of problems that can be solved using them. The fields of cryptography and computer security involve studying the means 
            for secure communication and preventing security vulnerabilities. Computer graphics and computational geometry address the generation of images.
              Programming language theory considers different ways to describe computational processes, and database theory concerns the manage
            ment of repositories of data. Human–computer interaction investigates the interfaces through which humans and computers interact, and 
            software engineering focuses on the design and principles behind developing software. Areas such as operating systems, networks and 
            embedded systems investigate the principles and design behind complex systems. Computer architecture describes the construction of computer components and 
            computer-operated equipment. Artificial intelligence and machine learning aim to synthesize goal-orientated processes such as problem-solving, decision-making, 
            environmental adaptation, planning and learning found in humans and animals. Within artificial intelligence, computer vision aims to understand and process 
            image and video data, while natural language processing aims to understand and process textual and linguistic data.
            The fundamental concern of computer science is determining what can and cannot be automated.[2][8][3][9][10] The Turing Award is generally recognized as 
            the highest distinction in computer science.[11][12]''',
            "details": {
                "title": "Human Impact on Climate Change",
                "authors": ["Jane Smith", "Alan Doe"],
                "year": 2022,
                "citations": 134,
                "url": "https://doi.org/fake1"
            }
        }
        time.sleep(1)
        return fake_json2


        

user_input = f"""
                  Claim:
                    Tariffs on imported goods always protect local jobs and boost domestic businesses.

                    Requested style:
                    Academic

                    Requested length:
                    Long

                    """





'''
agent = Agent()
agent.debug_get_agent_response(user_input,agent.research_Agent)
res = agent.research_agent_response(claim=user_input)
print(res)
print(res['details'])
print(res[
    'counter_argument'])
'''