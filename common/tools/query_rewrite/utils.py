import os
from typing import List, Dict, Any, Union
import json

from common.tools.search.classes import SearchQueryFormat
from common.utils.genai import get_aoai_client, call_llm

def generate_enhanced_query(chat_history: List[Dict[str, str]]) -> str:
    """
    Generate an enhanced search query based on the chat history.
    
    Args:
        chat_history (List[Dict[str, str]]): List of chat message dictionaries
        
    Returns:
        str: Enhanced search query optimized based on conversation context
    """
    client = get_aoai_client()
    
    # Extract the latest user query
    latest_query = chat_history[-1]["content"] if chat_history[-1]["role"] == "user" else ""
    
    # Build the conversation context - only use last 5 messages for efficiency
    previous_messages = chat_history[-6:-1] if len(chat_history) > 6 else chat_history[:-1]
    conversation_context = ""
    
    for msg in previous_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_context += f"{role}: {msg['content']}\n\n"
    
    # Create the prompt for generating the search query
    system_prompt = "You are a search query optimization assistant. Your task is to create the best possible search query to retrieve relevant documents."
    user_prompt = (
        f"Based on the following conversation, create an optimized search query to retrieve relevant documents that will help answer the user's latest question."
        f"Previous conversation: "
        f"{conversation_context}"
        f"User's latest question: "
        f"{latest_query}"
        f"\n\n"
        f"Return ONLY the optimized search query text. Do not include any JSON formatting, explanations, prefixes, or quotes. The output should be ready to use directly as a search query."
    )

    # Create a chat history list containing only the user prompt
    messages = [{"role": "user", "content": user_prompt}]
    
    # Call the utility function
    result = call_llm(
        client,
        system_prompt,
        messages,
        model=os.getenv("4o"),
        temperature=0.3,
        max_tokens=100,
        response_format=SearchQueryFormat
    )
    
    # Extract the enhanced query
    enhanced_query = extract_enhanced_query(result)
    
    print(f"Original query: '{latest_query}'")
    print(f"Enhanced query: '{enhanced_query}'")
    
    return enhanced_query


def extract_enhanced_query(result: Any) -> str:
    """
    Extract the enhanced query string from various possible result formats.
    
    Args:
        result: The result from LLM call, could be string, object, or JSON
        
    Returns:
        str: The extracted enhanced query string
    """
    # If result is an object with enhanced_query attribute
    if hasattr(result, "enhanced_query"):
        return extract_from_json_if_needed(result.enhanced_query)
    
    # If result is a string
    if isinstance(result, str):
        return extract_from_json_if_needed(result)
    
    # Fallback: convert to string
    return str(result)


def extract_from_json_if_needed(text: Union[str, Any]) -> str:
    """
    Try to extract enhanced_query from JSON string if applicable.
    
    Args:
        text: Potential JSON string or direct value
        
    Returns:
        str: The extracted enhanced_query or original text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Check if it's a JSON string
    stripped_text = text.strip()
    if stripped_text.startswith("{") and stripped_text.endswith("}"):
        try:
            json_obj = json.loads(stripped_text)
            if isinstance(json_obj, dict) and "enhanced_query" in json_obj:
                return json_obj["enhanced_query"]
        except json.JSONDecodeError:
            pass
    
    return text


