from google.adk.agents import Agent

content_agent = Agent(
    name="content_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant that generates content for a podcast.",
    description="Generates content for a podcast.",
)
