import os
import time
import google.auth
from google.adk.agents import Agent
from google import genai
from google.cloud import storage
from google.genai import types
from io import BytesIO
from google.adk.tools import load_artifacts

from image_agent.prompts import inital_prompt
from image_agent.tools import generate_image


_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


root_agent = Agent(
    name="thumbnail_agent",
    model="gemini-2.5-flash",
    instruction=inital_prompt,
    tools=[generate_image, load_artifacts],
)