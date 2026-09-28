from langchain_community.tools import DuckDuckGoSearchRun,WikipediaQueryRun
#from langchain_community.retrievers import WikipediaRetriever
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.utilities import WikipediaAPIWrapper


api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1500)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
search_tool = DuckDuckGoSearchRun()
#wiki_retriever = WikipediaRetriever()

# Lazy-loaded only for Research agent (logical_fallacies_retriever).
# This avoids connecting to Ollama / loading FAISS on startup for Fast/Web agents.
_db_retriever = None

def _get_db_retriever():
    global _db_retriever
    if _db_retriever is None:
        embedding_model = OllamaEmbeddings(model="qwen3-embedding:0.6b")
        vector_db = FAISS.load_local(
            "/home/gz/Documents/Rebuttal AI/Agent/Logical_Fallacies_DB",
            embedding_model,
            allow_dangerous_deserialization=True,  # trusted local DB only
        )
        _db_retriever = vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 2},
        )
    return _db_retriever

@tool
def search(query:str) -> str:
    """
    Search the web for current facts, events, news, or general information.
    """
    return search_tool.invoke(query)
'''
@tool
def wiki_summary(query: str, num_chars: int = 3000) -> str:
    """
    Retrieve a concise summary of a topic from Wikipedia.

    Args:
        query: Topic or entity to search for.
        num_chars: Maximum number of characters to return.
    """
    docs = wiki_retriever.invoke(query)
    if not docs:
        return "No Wikipedia results found."

    combined_text = "\n\n".join(doc.page_content for doc in docs)
    return combined_text[:num_chars]
'''

@tool
def wiki_summary(query: str) -> str:
    """
    Retrieve a concise summary of a topic from Wikipedia.

    Args:
        query: Topic or entity to search for.
        
    """
    try:
        docs = wikipedia_tool.run(query)

        if not docs:
            return "No Wikipedia results found."

     
        return str(docs)[:1500]

    except Exception as e:
        return f"Wikipedia lookup failed: {e}"
   
    
@tool
def logical_fallacies_retriever(query: str) -> str:
    """
    Retrieve definitions and examples of logical fallacies relevant to an argument or description.
    """
    db_retriever = _get_db_retriever()
    docs = db_retriever.invoke(query)
    if not docs:
        return "No matching logical fallacies found."

    
    return "\n\n".join(doc.page_content for doc in docs)[:1500]

@tool 
def get_json(details:str,response:str) -> dict:
    """
    returns python dictionary witt details and response

    Args:
        response: takes the counter argument to the claim as str.
        details: takes details assosiated with the coutner argument as str.
    """
    return {
        'response':response,
        'details': details 
    }


