import os

from google.adk.models import LlmResponse, LlmRequest
from google.adk.agents.callback_context import CallbackContext
import google.auth
from google.adk.agents import Agent
from google.adk.tools import google_search

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

chapter_length = "max. 5000 characters"
core_objective = "To educate the audience about the topics and keywords"
format = "episodic"
keywords = ["AI", "Technology", "Science", "Culture", "Society", "Future", "Innovation"]
language = "English"
length = "30 minutes"
speakers = "2"
target_age = "5-10"
target_audience = "kids"
topics = "To educate the audience about the topics and keywords"
type = "podcast"
# narrator = "John Doe"
# narrator_gender = "male"
# narrator_age = "30"

improvement_prompt = """
This podcast was already created: {podcast}.
Refine the podcast script based on the user's feedback.
"""

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    print("llm_request", llm_request)
    if callback_context.state.get("podcast"):
        llm_request.config.system_instruction = improvement_prompt.format(
            podcast=callback_context.state.get("podcast"), # TODO: get podcast from database
        )
    

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse):
    callback_context.state["podcast_refinement"] = llm_response.content.parts[0].text
    print("callback_context", callback_context, "llm_response", llm_response.content)

root_agent = Agent(
    name="content_refinement_agent",
    description="I am an agent specialized in refining podcast scripts.",
    model="gemini-2.5-flash",
    instruction="Refine podcast according to the user's feedback",
    tools=[google_search],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback
)