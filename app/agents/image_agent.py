from google.adk.agents import Agent

image_agent = Agent(
    name="image_agent",
    model="gemini-2.5-flash",
    description="Generates images for a podcast.",
    instruction="You are an AI Agent that generates the promt for an image for a podcast and iterate with the user until the user is satisfied.",
)
