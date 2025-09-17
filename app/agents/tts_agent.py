from google.adk.agents import Agent
from app.tools.tts_tool import tts_tool
from pydantic import BaseModel, Field

tts_agent = Agent(
    name="tts_agent",
    model="gemini-2.5-flash",
    instruction="""
        You are a helpful AI assistant that generates text to speech for a podcast.
        Use the content and the tool tts_tool to generate the audio.
    """,
    description="Generates text to speech for a podcast.",
    tools=[tts_tool]
)
