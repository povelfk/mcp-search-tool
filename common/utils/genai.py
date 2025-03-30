import openai
import os
import inspect
from typing import List, Dict, Any, Type

from common.tools.search.classes import SearchQueryFormat, SearchResultFormat

def get_aoai_client() -> openai.AzureOpenAI:
    client = openai.AzureOpenAI(
        azure_endpoint=os.getenv("AOAI_ENDPOINT"), 
        api_key=os.getenv("AOAI_KEY"),  
        api_version=os.getenv("AOAI_API_VERSION"),
    )
    return client

def call_llm(client, system_message: str, chat_history: List[Dict[str, str]], **kwargs):
    response_format = kwargs.get('response_format')

    default_params = {
        'model': os.getenv("4o"),
        'temperature': 0.3,
        'max_tokens': 800
    }

    params = {**default_params, **kwargs}
    messages = [
        {"role": "system", "content": system_message},
        *chat_history,
    ]

    if inspect.isclass(response_format):
        # Use beta client with parse method if response_format is a class
        try:
            response = client.beta.chat.completions.parse(
                messages=messages,
                **params
            )
            # If response is already parsed to the expected class, return it directly
            if isinstance(response, response_format):
                return response
            # If it's a dict, convert it to the expected class
            elif isinstance(response, dict):
                return response_format(**response)
            # If it's a standard response object, extract content
            else:
                return response_format(enhanced_query=response.choices[0].message.content)
        except Exception as e:
            # Fallback in case of parsing error
            print(f"Error parsing response: {e}")
            standard_response = client.chat.completions.create(
                messages=messages,
                **{k: v for k, v in params.items() if k != 'response_format'}
            )
            return response_format(enhanced_query=standard_response.choices[0].message.content)
    else:
        # Otherwise, use standard client method
        response = client.chat.completions.create(
            messages=messages,
            **params
        )
        return response.choices[0].message.content

