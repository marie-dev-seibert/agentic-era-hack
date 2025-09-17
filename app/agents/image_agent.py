from google.adk.agents import Agent

image_agent = Agent(
    name="image_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant that generates images for a podcast.",
    description="Generates images for a podcast.",
)
