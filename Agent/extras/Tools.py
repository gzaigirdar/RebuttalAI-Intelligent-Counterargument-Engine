from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.retrievers import WikipediaRetriever
from langchain.tools import tool
from langchain_community.vectorstores import FAISS 
from langchain_community.embeddings import OllamaEmbeddings



class AgentTools:


    def __init__(self):

        self.search_tool =  DuckDuckGoSearchRun()
        self.WikiRetriever = WikipediaRetriever()
        self.embedding_Model =  OllamaEmbeddings(model='qwen3-embedding:0.6b')
        self.Vector_DB = FAISS.load_local('/home/gz/Documents/Rebuttal AI/Agent/Logical_Fallacies_DB',self.embedding_Model,allow_dangerous_deserialization=True)
        self.DB_Retriever = self.Vector_DB.as_retriever(
            search_type = "similarity",
            search_kwargs = {"k":2}

        )
        
        @tool
        def search(query):
            """
            This is tool is a searches the web for facts,events,news,and other live information.
            Args:
            search term
            """
            return self.search_tool.run(query)
        
        @tool
        def WikiSummary(query,num_chars=3000):
            """
            This tool takes any topic,event,person returns information from wikipedia.
            If more information need then num_chars arguments should be pass. The default is 3000 characters

            Args:
            query: Search terms to look for
            limit: Maximum number of results to return
            num_chars: maxium number of chracters returned, default is 3000. if needed then incrase it. 
            """
            docs = self.WikiRetriever.invoke(query) 
            if not docs:
                return "No results found."
            return docs[0].page_content[:num_chars]
           
        @tool
        def logical_fallacies_retriver(query):
            """
            retrives documents that about logical fallacies from vector db
            """
            docs = self.DB_Retriever.invoke(query)
            return "\n\n".join(doc.page_content for doc in docs)
        
        
        self.search = search
        self.Wiki_Summary = WikiSummary
        self.Logical_fallacies_retriver = logical_fallacies_retriver  

        def gather_information(info):
            if 'search' in info:
                search_topic = info['search']
                search_info = self.search.run(search_topic)  
            else:
                search_info = ''
            if 'WikiSummary' in info:
                wiki_topic = info['WikiSummary']
                wiki_info = self.Wiki_Summary.run(wiki_topic)
            else:
                wiki_info = ' '

            if 'Logical_fallacies_retriver' in info:
                fallacies_topic = info['Logical_fallacies_retriver']
                fallacies_info = self.Logical_fallacies_retriver.run(fallacies_topic)
            else:
                fallacies_info = ' '
            return search_info + '\n\n' + wiki_info + '\n\n' + fallacies_info + '\n'
        
        self.research = gather_information

