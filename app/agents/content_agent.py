from google.adk.agents import Agent
from google.adk.models import LlmRequest
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents import Agent
from google.adk.tools import ToolContext

from pydantic import BaseModel, Field

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
    speaker_names: list[str] = Field(description="The names of the speakers")

def formatted_output(tool_context: ToolContext, podcast: Podcast):
    """
    Returns the audio script of the correctly formatted podcast.

    Args:
        audio_script: Podcast
    
    Returns:
        Podcast - The formatted output of the podcast. For example:
        {audio_script: [{"chapter_title": "Chapter 1", "chapter_content": "Chapter 1 content"}, {"chapter_title": "Chapter 2", "chapter_content": "Chapter 2 content"}], "title": "Podcast Title"}
    """
    tool_context.state["podcast"] = podcast
    return podcast

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    llm_request.config.system_instruction = initial_prompt

initial_prompt = """
You are an agent specialized in creating audio content scripts. After audio script creation ask the user if he wants to continue by exiting to your parent agent (the root agent).
You are an AIs Agent that generates content for a {type} audio script and iterate with the user until the user is satisfied.
Strictly follow the user's inputs and constraints.
The formatting of the audio script should have the host's name with an optional emotion in which the text should be delivered.
Between the host name and text should be a colon.
That would be something like this:
Alex excited: Hello, how are you?
Zara bored: I'm good, thank you. How about you?
Alex: I'm good too, thank you.
Zara: What are you doing?
Alex: I'm doing nothing.
Zara serious: Be honest, what are you doing?

Constraints:
- Language: write everything in English.
- Format: {format}. Structure the episode with a clear beginning, multiple chapters, and an outro.
- Speakers: {speakers}.
- Audience: {target_audience}, ages {target_age}. Use a friendly, engaging, age-appropriate tone.
- Core objective: {core_objective}.
- Topics to cover: {topics}.
- Keywords to weave in naturally: {keywords}.

Deliverable:
Scripted episode (ready to record):
   - Chapter 0: intro and host greeting, max. 5000 characters.
   - Chapter 1: clear subheading, main content, max. 5000 characters.

Writing guidelines:
- Keep sentences short and vocabulary simple; briefly explain any complex term in simple language.
- Add optional speaker emotion after host name (e.g., bored, excited, serious, etc.).
- Smooth transitions between chapters; avoid abrupt topic changes.
- Be inclusive and positive; avoid sensitive or unsafe content.
- If any input is missing, make reasonable, child-safe assumptions consistent with the objective.

Always return the whole script content described above (also on refinement steps) and ask the user if they are satisfied with the script.
If user is not satisfied, iterate with the user until the user is satisfied.
If user is satisfied, this is your final response and your turn is completed.
"""

content_agent = Agent(
    input_schema=PodcastInput,
    name="content_creation_agent",
    description="I am an agent specialized in creating audio content scripts. After audio script creation ask the user if he wants to continue by exiting to your parent agent (the root agent).",
    model="gemini-2.5-flash",
    instruction="Create a podcast based on user's inputs",
    tools=[formatted_output],
    before_model_callback=before_model_callback,
    # output_key="podcast",
)

# educational
# 3 speakers, 1 host and 2 guests
# Target Audience: kids
# Target Age: 5-10
# Core Objective: educate about science and entertain with stories
# Topics to cover: science and stories
# speaker names: Alex, Zara and Mia
# science and stories



#    - Chapter 2: clear subheading, main content, max. 5000 characters.
#    - Chapter 3: clear subheading, main content, max. 5000 characters.
#    - Chapter 4: Fun fact segment (kid-friendly), max. 5000 characters.
#    - Chapter 5: Recap of key points, max. 5000 characters.
#    - Chapter 6: Call-to-action (age-appropriate), max. 5000 characters.
#    - Chapter 7: Outro and credits, max. 5000 characters.