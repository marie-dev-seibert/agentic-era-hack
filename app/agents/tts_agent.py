from google.adk.agents import Agent

tts_agent = Agent(
    name="tts_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant that generates text to speech for a podcast.",
    description="Generates text to speech for a podcast.",
)
