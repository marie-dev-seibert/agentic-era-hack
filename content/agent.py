import os

from google.adk.models import LlmResponse
from google.adk.agents.callback_context import CallbackContext
import google.auth
from google.adk.agents import Agent
from google.adk.tools import google_search

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

def log(callback_context: CallbackContext, llm_response: LlmResponse):
    print(llm_response.content)

# def create_podcast_script(query: str):
#     """
#     Create a podcast script based on the user's query.

#     Args:
#         query: topics, keywords, and any other information about the podcast.

#     Returns:
#         A string with the podcast script.
#     """

root_agent = Agent(
    name="content_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant designed to create a podcast with multiple chapters with the provided information of the user.",
    tools=[google_search],
    after_model_callback=log
)