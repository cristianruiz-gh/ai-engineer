from agents import Agent, WebSearchTool, ModelSettings
from dotenv import load_dotenv
import os
load_dotenv(override=True)
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY") 
os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="llama-3.3-70b-versatile",
    model_settings=ModelSettings(tool_choice="required"),
)