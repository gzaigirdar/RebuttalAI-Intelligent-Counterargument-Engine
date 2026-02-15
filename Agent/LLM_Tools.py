from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.retrievers import WikipediaRetriever
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings


search_tool = DuckDuckGoSearchRun()
wiki_retriever = WikipediaRetriever()
embedding_model = OllamaEmbeddings(model="qwen3-embedding:0.6b")

vector_db = FAISS.load_local(
    "/home/gz/Documents/Rebuttal AI/Agent/Logical_Fallacies_DB",
    embedding_model,
    allow_dangerous_deserialization=True,  # trusted local DB only
)

db_retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2},
)

@tool
def search(query):
    """
    Search the web for current facts, events, news, or general information.
    """
    return search_tool.invoke(query)

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

@tool
def logical_fallacies_retriever(query: str) -> str:
    """
    Retrieve definitions and examples of logical fallacies relevant to an argument or description.
    """
    docs = db_retriever.invoke(query)
    if not docs:
        return "No matching logical fallacies found."

    return "\n\n".join(doc.page_content for doc in docs)
@tool 

def get_json(details:str,counter_argument:str) -> dict:
    """
    returns python dictionary witt details and counter argument

    Args:
        counter_argument: takes the counter argument to the claim as str.
        details: takes details assosiated with the coutner argument as str.
    """
    return {
        'counter_argument':counter_argument,
        'details': details 
    }