# Web Search Agent MCP Tool

An MCP (Microsoft Copilot Plugin) tool that enhances search queries based on conversation context and returns web search results.

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher

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
