import os

from google.adk.models import LlmResponse, LlmRequest
from google.adk.agents.callback_context import CallbackContext
import google.auth
from google.adk.agents import Agent
from google.adk.tools import google_search, ToolContext
from google.adk.sessions.in_memory_session_service import InMemorySessionService

from content_creation.prompt import initial_prompt
from pydantic import BaseModel, Field

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

class PodcastInput(BaseModel):
    core_objective: str = Field(description="The core objective of the podcast")
    format: str = Field(description="The format of the podcast")
    keywords: list[str] = Field(description="The keywords of the podcast")
    speakers: int = Field(description="The amount of speakers in the podcast")
    target_age: str = Field(description="The target age of the podcast")
    target_audience: str = Field(description="The target audience of the podcast")
    topics: str = Field(description="The topics of the podcast")
    type: str = Field(description="The type of the podcast")

class Chapter(BaseModel):
    chapter_title: str = Field(description="The title of the chapter")
    chapter_content: str = Field(description="The content of the chapter")

class Podcast(BaseModel):
    audio_script: list[Chapter]
    title: str = Field(description="The title of the podcast")

def formatted_output(tool_context: ToolContext, podcast: Podcast):
    """
    Returns the audio script of the correctly formatted podcast.

    Args:
        audio_script: {audio_script: [{"chapter_title": "Chapter 1", "chapter_content": "Chapter 1 content"}, {"chapter_title": "Chapter 2", "chapter_content": "Chapter 2 content"}], "title": "Podcast Title"} - The audio script of the podcast
    
    Returns:
        Podcast - The formatted output of the podcast. For example:
        {audio_script: [{"chapter_title": "Chapter 1", "chapter_content": "Chapter 1 content"}, {"chapter_title": "Chapter 2", "chapter_content": "Chapter 2 content"}], "title": "Podcast Title"}
    """
    tool_context.state["podcast"] = podcast
    return podcast

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    llm_request.config.system_instruction = initial_prompt

root_agent = Agent(
    input_schema=PodcastInput,
    name="content_creation_agent",
    description="I am an agent specialized in creating audio content scripts.",
    model="gemini-2.5-flash",
    instruction="Create a podcast based on user's inputs",
    tools=[formatted_output],
    before_model_callback=before_model_callback,
)