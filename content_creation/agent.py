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

max_chapter_length = "max. 5000 characters"
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

class PodcastInput(BaseModel):
    max_chapter_length: int = Field(description="The maximum length of the chapter in characters")
    core_objective: str = Field(description="The core objective of the podcast")
    format: str = Field(description="The format of the podcast")
    keywords: list[str] = Field(description="The keywords of the podcast")
    language: str = Field(description="The language of the podcast")
    length: str = Field(description="The length of the podcast")
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
        max_chapter_length=max_chapter_length,
        speakers=speakers,
    )

root_agent = Agent(
    input_schema=PodcastInput,
    name="content_creation_agent",
    description="I am an agent specialized in creating audio content scripts.",
    model="gemini-2.5-flash",
    instruction="Create a podcast",
    tools=[formatted_output],
    before_model_callback=before_model_callback,
)