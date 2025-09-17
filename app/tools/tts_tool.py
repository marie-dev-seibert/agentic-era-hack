from google.genai import types
from pydantic import BaseModel, Field

class Chapter(BaseModel):
    chapter_title: str = Field(description="The title of the chapter")
    chapter_content: str = Field(description="The content of the chapter")

class Podcast(BaseModel):
    audio_script: list[Chapter]
    title: str = Field(description="The title of the podcast")

def tts_tool(podcast: Podcast):
    """Generates text to speech for a podcast."""

    # Read the audio file
    with open("out/output_0.wav", "rb") as audio_file:
        audio_bytes = audio_file.read()

    audio_artifact = types.Part.from_bytes(
        data=audio_bytes, mime_type="audio/wav"
    )

    return audio_artifact
