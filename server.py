from mcp.server.fastmcp import FastMCP
from typing import List, Dict
import json
import sys
import os
import signal
from dotenv import load_dotenv

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Load environment variables from .env file using absolute path
load_dotenv(os.path.join(current_dir, ".env"))

# Import from the new structure
from common.tools.query_rewrite.utils import generate_enhanced_query
from common.tools.search.utils import web_search

def signal_handler(signal, frame):
    """
    Signal handler to gracefully handle termination signals.
    """
    print("Signal handler called with signal:", signal)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

mcp = FastMCP(
    name="web search 🚀"
)

@mcp.tool()
def enhanced_search_query(chat_history: List[Dict[str, str]]) -> str:
    """
    Generate an enhanced search query based on the chat history.
    
    Args:
        chat_history (List[Dict[str, str]]): List of chat message dictionaries
        
    Returns:
        str: Enhanced search query optimized based on conversation context
    """
    return generate_enhanced_query(chat_history)

@mcp.tool()
def search_web(search_query: str) -> str:
    """
    Perform a web search using the Tavily API and return the results as a JSON string.

    Args:
        search_query (str): The query to search for.

    Returns:
        str: A JSON string containing search results with query, title, url, and snippet.
    """
    return web_search(search_query)

@mcp.tool()
def perform_web_search(chat_history: List[Dict[str, str]]) -> str:
    """
    Performs an enhanced web search using the Tavily API.
    
    We start by generating an enhanced search query from the chat history.
    After that, we use the enhanced query to search for relevant information.
    Lastly, the results are returned as a JSON string.
    
    Args:
        chat_history (List[Dict[str, str]]): The conversation history. Each message must include both
                                            "role" (either "user" or "assistant") and "content" keys.
                                            Example: [{"role": "user", "content": "question text"}]
        
    Returns:
        str: JSON string with search results
    """
    try:
        # Validate the chat history format
        if not all("role" in msg and "content" in msg for msg in chat_history):
            raise ValueError("Each message in chat_history must contain 'role' and 'content' keys")
            
        query = generate_enhanced_query(chat_history)
        return web_search(query)
    except Exception as e:
        error_result = {"error": str(e), "results": []}
        return json.dumps(error_result)

def test_search():
    """Test function to verify search functionality"""
    messages = [
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": "What is the population of Paris?"}
    ]
    perform_web_search(messages)
    # print(perform_web_search(messages))

# Main entry point for running the server
if __name__ == "__main__":
    # For testing, uncomment the line below:
    # test_search()
    
    # Run the MCP server
    print("Starting MCP server...")
    mcp.run(transport="stdio")