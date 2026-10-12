# Get API key from .env file
from dotenv import load_dotenv
load_dotenv()

# Basic langchain imports
from langchain.agents import create_agent
from langchain.tools import tool

# from pathlib import Path
# from langchain.mcp import MCPAdapter

# from fastmcp import FastMCP
# mcp = FastMCP("Network Name")


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    # Above doc string informs agent on the use of the function
    # and tells it to interpret it as a tool.
    
    return f"It's always sunny in {city}!"

def get_prompt() -> str:

    prompt = input("INPUT: ")
    return prompt

agent = create_agent(
    model="google_genai:gemini-flash-lite-latest",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

def main():

    prompt = get_prompt()

    result = agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]}
    )
    
    print(result["messages"][-1].text)


# from langchain.agents import create_agent
# from langchain.mcp import MCPAdapter


# async def main():
#     async with MCPAdapter("https://example.com/mcp") as adapter:
#         tools = await adapter.list_tools()
#         agent = create_agent("claude-sonnet-5", tools)
#         return await agent.ainvoke({"messages": [{"role": "user", "content": "..."}]})


if __name__ == "__main__":
    main()