from pydantic import BaseModel, Field
from typing import Dict, List

# ------------------------------------------------------
# Input classes for external LLM calls via mcp.run(args_schema=)
# These classes define the expected input structure for LLM functions
# ------------------------------------------------------

class GenerateEnhancedQueryInput(BaseModel):
    chat_history: List[Dict[str, str]] = Field(
        ...,
        description="A list of dictionaries representing the chat history, where each dictionary contains key-value pairs of strings."
    )
