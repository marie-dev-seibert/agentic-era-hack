from google.adk.agents import Agent
from app.prompts.inital_image_prompt import inital_image_prompt
from app.tools.generate_image_tool import generate_image


image_agent = Agent(
    name="image_agent",
    model="gemini-2.5-flash",
    instruction=inital_image_prompt,
    description="You are an AI Agent that generates image for a podcast and iterate with the user until the user is satisfied. After Image creation ask the user if he wants to continue with the podcast generation process and exit to your parent agent",
    tools=[generate_image],
    # output_key="output_image",
)