import json
import os
from tavily import TavilyClient

def web_search(search_query: str) -> str:
    """
    Perform a web search using the Tavily API and return the results as a JSON string.

    Args:
        search_query (str): The query to search for.

    Returns:
        str: A JSON string containing search results with query, title, url, and snippet.
    """
    try:
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        max_results = 3
        response = tavily_client.search(search_query, max_results=max_results)
        
        # Ensure we have a Python dict before converting to JSON string
        result_dict = response if isinstance(response, dict) else json.loads(response)
        
        # Convert to JSON string for LLM consumption
        return json.dumps(result_dict, indent=2)
    except Exception as e:
        error_result = {"error": str(e), "results": []}
        return json.dumps(error_result)
