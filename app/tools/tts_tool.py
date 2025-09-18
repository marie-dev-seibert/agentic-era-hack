from io import BytesIO
import wave
from google import genai
from google.adk.tools import ToolContext
from google.cloud import storage
from google.genai import types
from pydantic import BaseModel
import random
from pydantic import BaseModel, Field
import google.auth
import os
import time

from app.agents.utils.voices import VOICE_NAMES


_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), vertexai=False)

class Chapter(BaseModel):
    chapter_title: str = Field(description="The title of the chapter")
    chapter_content: str = Field(description="The content of the chapter")

class Podcast(BaseModel):
    audio_script: list[Chapter]
    title: str = Field(description="The title of the podcast")
    speaker_names: list[str] = Field(description="The names of the speakers")


def create_speaker(speaker_name: str) -> types.SpeakerVoiceConfig:
    """
    Create a SpeakerVoiceConfig for the given speaker and voice_name.

    Args:
        speaker_name (str): The name/label for the speaker (e.g., "Speaker01").
        voice_name (str): The name of the voice to use. Must be one of the keys in VOICE_NAMES.

    Returns:
        types.SpeakerVoiceConfig: The speaker voice config for Gemini TTS.

    Raises:
        ValueError: If the voice_name is not a valid key in VOICE_NAMES.
    """
    # Pick a random voice from the VOICE_NAMES keys if the provided voice_name is not valid
    voice_name = random.choice(list(VOICE_NAMES.keys()))

    return types.SpeakerVoiceConfig(
        speaker=speaker_name,
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name=speaker_name,
            )
        ),
    )


async def tts_tool(tool_context: ToolContext) -> dict[str, str]:
    """Generates text to speech for a podcast."""
    speaker_names = tool_context.state["podcast"]["speaker_names"]
    chapter_texts = [chapter["chapter_content"] for chapter in tool_context.state["podcast"]["audio_script"]]
    text = "\n".join(chapter_texts)

    speaker_voice_configs = [create_speaker(speaker_name) for speaker_name in speaker_names]

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=speaker_voice_configs,
                )
            ),
        ),
    )

    data = response.candidates[0].content.parts[0].inline_data.data
    if data is None:
        raise ValueError("No audio data received from Gemini TTS")
    
    artifact_name = f"generated-audio_{int(time.time())}.wav"
    create_wav_file(artifact_name, data)  # Saves the file to current directory
    wav_data = upload_audio_to_gcs(tool_context, data)
    
    report_artifact = types.Part.from_bytes(
            data=wav_data, mime_type="audio/wav"
        )

    await tool_context.save_artifact(artifact_name, report_artifact)

    return {
        "status": "success",
        "artifact_name": artifact_name,
        "message": "Successfully synthesized speech."
    }


def create_wav_file(filename: str, pcm: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
    dirname = os.path.dirname("/out")
    if dirname: 
        os.makedirs(dirname, exist_ok=True)
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def upload_audio_to_gcs(tool_context: ToolContext, audio_content: bytes):
    print("Uploading audio to GCS")
    bucket_name = "qwiklabs-gcp-03-d90b22626152-aiqueens-audio-data"
    destination_blob_name = f"{time.time()}/output.wav"

    wav_buffer = BytesIO()
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(24000)
        wf.writeframes(audio_content)
    
    wav_data = wav_buffer.getvalue()
    
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(wav_data, content_type="audio/wav")

    gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
    tool_context.state["generated_audio_gcs_uri_" + str(int(time.time()))] = gcs_uri

    return wav_data



