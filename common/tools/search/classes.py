from pydantic import BaseModel, Field

# ------------------------------------------------------
# Input classes for external LLM calls via mcp.run(args_schema=)
# These classes define the expected input structure for LLM functions
# ------------------------------------------------------

class WebSearchInput(BaseModel):
    search_query: str = Field(..., description="The query string to search for.")

# ------------------------------------------------------
# Format classes for internal LLM calls
# These classes define the expected response structure from internal LLM operations
# ------------------------------------------------------

class SearchQueryFormat(BaseModel):
    enhanced_query: str = Field(..., description="The enhanced or refined search query", example="What is supervised learning?")

class SearchResultFormat(BaseModel):
    query: str = Field(..., description="The original search query", example="Machine learning basics")
    title: str = Field(..., description="Title of the search result item", example="Introduction to Machine Learning")
    url: str = Field(..., description="URL link to the search result", example="https://example.com/machine-learning")
    snippet: str = Field(..., description="Brief snippet or summary of the search result", example="Machine learning is a subset of artificial intelligence...")
