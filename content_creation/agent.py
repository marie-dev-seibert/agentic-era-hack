import os

from google.adk.models import LlmResponse, LlmRequest
from google.adk.agents.callback_context import CallbackContext
import google.auth
from google.adk.agents import Agent
from google.adk.tools import google_search

from content_creation.prompt import initial_prompt

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

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    # TODO: replace variables
    llm_request.config.system_instruction = initial_prompt.format(
        core_objective=core_objective,
        language=language,
        type=type,
        topics=topics,
        keywords=keywords,
        format=format,
        target_audience=target_audience,
        target_age=target_age,
        length=length,
        chapter_length=chapter_length,
        speakers=speakers,
    )
        

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse):
    callback_context.state["podcast"] = llm_response.content.parts[0].text
    print("callback_context", callback_context, "llm_response", llm_response.content)

root_agent = Agent(
    name="content_creation_agent",
    description="I am an agent specialized in creating audio content scripts.",
    model="gemini-2.5-flash",
    instruction="Create a podcast",
    tools=[google_search],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback
)