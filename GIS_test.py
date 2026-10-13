import json
import zipfile
from getpass import getpass

from langchain.agents import create_agent
from langchain.tools import tool


from dotenv import load_dotenv
load_dotenv()

# Open sourced mcp workaround
# io.github.muend/arcgis-mcp-bridge


def history_from_aprx(aprx: str) -> list[dict]:
    """gets the geoprocessing history from an arcgis pro aprx file annd returns each item in the history"""
    with zipfile.ZipFile(aprx) as zf:  # an aprx is a zipfile
        with zf.open('GISProject.json') as j:  # geoprocessing history is stored in this file
            jd = json.loads(j.read())
    return [d for d in jd['projectItems'] if d.get('itemType') == 'GPHistory']

agent = create_agent(
    model="google_genai:gemini-flash-lite-latest",
    tools=[history_from_aprx],
    system_prompt="You are a text generation AI that interprets geoprocessing history objects from ArcGIS Pro. |" \
    "Provide a concise natural language summary of the geoprocessing history object with no additional commentary."
)


aprxf = r"D:\450_SocialSciences\W04\EnvironmentalJustice_Isaacbean\EnvironmentalJustice_Isaacbean.aprx"
history = history_from_aprx(aprxf)

# chain = ChatPromptTemplate.from_messages(
#     [
#         ('system', 'You are a text generation AI that interprets geoprocessing history objects from ArcGIS Pro. '
#                    'Provide a concise natural language summary of the geoprocessing history object with no additional commentary.'),
#         ('human', '```xml\n{propertiesXML}\n```')
#     ]
# ) | agent

# respsonses = agent.batch([dict(propertiesXML=h['propertiesXML']) for h in history])

requests = [
    {
        "messages": [
            {
                "role": "user",
                "content": f"```xml\n{h['propertiesXML']}\n```",
            }
        ]
    }
    for h in history
    if h.get("propertiesXML")
]

responses = agent.batch(requests)

summaries = [response["messages"][-1].text for response in responses]
print(summaries)