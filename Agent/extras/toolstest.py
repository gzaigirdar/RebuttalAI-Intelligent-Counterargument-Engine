from langchain_community.tools import WikipediaQueryRun,DuckDuckGoSearchRun,DuckDuckGoSearchResults
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from langchain_community.utilities.semanticscholar import SemanticScholarAPIWrapper
from langchain_community.retrievers import WikipediaRetriever
from langchain_community.utilities import WikipediaAPIWrapper

api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=2000)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
wiki_retriever = WikipediaRetriever()
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
#wiki = WikipediaAPIWrapper()
'''scholar_api_wrapper = SemanticScholarAPIWrapper(
    top_k_results=1,          # number of papers returned
    load_max_docs=1,          # max documents fetched
    doc_content_chars_max=2000,  # truncate long abstracts
    min_citations=2


)'''


#search_tool = DuckDuckGoSearchRun()
#search_result = DuckDuckGoSearchResults()
'''
result = search_tool.run("Minnesota Fraud 2025")
result2 = search_result.run('Minnesota Fraud 2025')
print(result)  # Prints a summary or relevant content from Wikipedia
print('---------------------------------------')
print('search with for information')
print(result2)
'''
from langchain_community.utilities.semanticscholar import SemanticScholarAPIWrapper

class CustomScholarTool:
    def __init__(self, top_k=5, min_citations=5, year_range=(2018, 2026), max_chars=2000):
        self.wrapper = SemanticScholarAPIWrapper(
            top_k_results=top_k,
            load_max_docs=top_k,
            doc_content_chars_max=max_chars,
            min_citations=min_citations
        )
        self.year_range = year_range

    
tool = CustomScholarTool(top_k=3, min_citations=10)
papers = tool.query("Human effect on climate change")

for p in papers:
    print(p["title"], "| Citations:", p["citations"], "| Year:", p["year"])
    print(p["abstract"][:500])  # print first 500 chars of abstract
    print("URL:", p["url"])
    print("-"*50)


