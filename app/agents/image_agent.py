import os
import google.auth
from google.adk.agents import Agent
from app.prompts.inital_image_prompt import inital_image_prompt
from app.tools.generate_image_tool import generate_image


_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

image_agent = Agent(
    name="thumbnail_agent",
    model="gemini-2.5-flash",
    instruction=inital_image_prompt,
    tools=[generate_image],
    output_key="output_image",
)