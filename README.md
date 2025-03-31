# Web Search Agent MCP Tool

Creates an MCP (Model Context Protocol) Web Search tool (Tavily) that generates search queries based on conversation context and returns web search results. This tool integrates with Azure OpenAI for query enhancement and works directly within VS Code.

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher
2. Azure OpenAI API access
3. Tavily API key
4. VS Code Insiders

### Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your API keys:
   ```
   AOAI_ENDPOINT=your_azure_openai_endpoint
   AOAI_KEY=your_azure_openai_key
   AOAI_API_VERSION=your_azure_openai_api_version
   4o=your_gpt4o_model_deployment_name
   TAVILY_API_KEY=your_tavily_api_key
   ```

### VS Code Configuration

1. Configure VS Code to Discover MCP Servers:
   - Open VS Code Insiders
   - Navigate to File > Preferences > Settings
   - In the search bar, type `mcp`
   - Locate the "Chat: Mcp Discovery Enabled" setting and ensure it is checked. This allows VS Code to detect MCP servers automatically

2. Add the following to your VS Code settings.json:
   ```json
   "mcp": {
       "inputs": [],
       "servers": {
           "web-search-tool": {
               "type": "stdio",
               "command": "<FULL PATH TO VIRTUAL ENV>",
               "args": [
                   "<FULL PATH TO PYTHON FILE>"
               ]
           }
       }
   }
   ```
3. To access the tool in VS Code:
   - Open the Chat view in VS Code
   - The web search tool will appear as an available extension in the chat interface
   - You can now use the web search capabilities directly within your coding environment
     

### Running the Tool

#### Development Mode
```bash
fastmcp dev server.py
```

#### Production Mode
```bash
python server.py
```

## Available Tools

- `enhanced_search_query`: Generate an optimized search query based on conversation context
- `search_web`: Perform a web search with Tavily
- `perform_web_search`: Combines query enhancement and web search in one step

## Troubleshooting

- **API Key errors**: Ensure all required environment variables are set in your `.env` file.
- **VS Code integration issues**: Verify that the paths in your settings.json are correct and that the MCP discovery setting is enabled.

