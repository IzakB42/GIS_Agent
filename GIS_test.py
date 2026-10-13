import json
import zipfile
from getpass import getpass

from langchain.agents import create_agent
from langchain.tools import tool

from langchain.mcp import MCPAdapter
import asyncio

# Gets api key from .env file
from dotenv import load_dotenv
load_dotenv()

# Open sourced mcp workaround
# io.github.muend/arcgis-mcp-bridge


# def history_from_aprx(aprx: str) -> list[dict]:
#     """gets the geoprocessing history from an arcgis pro aprx file annd returns each item in the history"""
#     with zipfile.ZipFile(aprx) as zf:  # an aprx is a zipfile
#         with zf.open('GISProject.json') as j:  # geoprocessing history is stored in this file
#             jd = json.loads(j.read())
#     return [d for d in jd['projectItems'] if d.get('itemType') == 'GPHistory']

# agent = create_agent(
#     model="google_genai:gemini-flash-lite-latest",
#     tools=[history_from_aprx],
#     system_prompt="You are a text generation AI that interprets geoprocessing history objects from ArcGIS Pro. |" \
#     "Provide a concise natural language summary of the geoprocessing history object with no additional commentary."
# )


aprxf = r"D:\450_SocialSciences\W04\EnvironmentalJustice_Isaacbean\EnvironmentalJustice_Isaacbean.aprx"
# history = history_from_aprx(aprxf)


# requests = [
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": f"```xml\n{h['propertiesXML']}\n```",
#             }
#         ]
#     }
#     for h in history
#     if h.get("propertiesXML")
# ]

def get_prompt() -> str:

    prompt = input("INPUT: ")
    return prompt

prompt = get_prompt()

CONFIG = {
  "mcpServers": {
    "docs-langchain": {
      "url": "https://docs.langchain.com/mcp"
    },
    "reference-langchain": {
      "url": "https://reference.langchain.com/mcp"
    }
  }
}

async def MCPGetter(config):
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent(
            model= "google_genai:gemini-flash-lite-latest", 
            tools= tools,
            system_prompt= "You are a text generation AI that interprets geoprocessing history objects from ArcGIS Pro. |" \
                "Provide a concise natural language summary of the geoprocessing history object with no additional commentary.")
        
        return await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})

async def main():
    response = await MCPGetter(CONFIG)
    print(response)

# Batch improves response time and decreases costs by running requrests simultaneously.
# responses = agent.batch(requests)

# summaries = [response["messages"][-1].text for response in responses]
# print(summaries)

if __name__ == "__main__":
    asyncio.run(main())