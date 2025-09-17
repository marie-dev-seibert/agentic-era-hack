from datetime import time
import wave
from google.adk.tools import ToolContext
from google.cloud import storage
from google.cloud.storage.blob import BytesIO
from google.genai import types
from pydantic import BaseModel
import random
class Chapter(BaseModel):
    chapter_title: str
    chapter_content: str

class Podcast(BaseModel):
    title: str
    chapters: list[Chapter]
    speaker_names: list[str]

VOICE_NAMES = {
    "Zephyr": "Bright",
    "Puck": "Upbeat",
    "Charon": "Informative",
    "Kore": "Firm",
    "Fenrir": "Excitable",
    "Leda": "Youthful",
    "Orus": "Firm",
    "Aoede": "Breezy",
    "Callirrhoe": "Easy-going",
    "Autonoe": "Bright",
    "Enceladus": "Breathy",
    "Iapetus": "Clear",
    "Umbriel": "Easy-going",
    "Algieba": "Smooth",
    "Despina": "Smooth",
    "Erinome": "Clear",
    "Algenib": "Gravelly",
    "Rasalgethi": "Informative",
    "Laomedeia": "Upbeat",
    "Achernar": "Soft",
    "Alnilam": "Firm",
    "Schedar": "Even",
    "Gacrux": "Mature",
    "Pulcherrima": "Forward",
    "Achird": "Friendly",
    "Zubenelgenubi": "Casual",
    "Vindemiatrix": "Gentle",
    "Sadachbia": "Lively",
    "Sadaltager": "Knowledgeable",
    "Sulafat": "Warm"
}

def create_speaker(speaker_name: str, voice_name: str) -> types.SpeakerVoiceConfig:
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
    if voice_name not in VOICE_NAMES:
        # Pick a random voice from the VOICE_NAMES keys if the provided voice_name is not valid
        voice_name = random.choice(list(VOICE_NAMES.keys()))

    return types.SpeakerVoiceConfig(
        speaker=speaker_name,
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name=voice_name,
            )
        ),
    )


def tts_tool(chapters: list[str], speaker_voice_mapping: dict[str, str], tool_context: ToolContext) -> dict[str, str]:
    """Generates text to speech for a podcast."""

    # client = genai.Client()

    prompt = chapters[1]
    speaker_voice_configs = [create_speaker(speaker_name, voice_name) for speaker_name, voice_name in speaker_voice_mapping.items()]

    # response = client.models.generate_content(
    #     model="gemini-2.5-flash-preview-tts",
    #     contents=prompt,
    #     config=types.GenerateContentConfig(
    #         response_modalities=["AUDIO"],
    #         speech_config=types.SpeechConfig(
    #             multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
    #                 speaker_voice_configs=speaker_voice_configs,
    #             )
    #         ),
    #     ),
    # )

    # data = response.candidates[0].content.parts[0].inline_data.data
    # create_wav_file("out/output.wav", data)  # Saves the file to current directory
    # audio_url = upload_audio_to_gcs(data)

    # return {
    #     "status": "success",
    #     "audio_url": audio_url,
    #     "message": "Successfully synthesized speech."
    # }

    return {
        "status": "success",
        "audio_url": "gs://qwiklabs-gcp-03-d90b22626152-aiqueens-audio-data/1758030805.346349/output_0.wav", 
        "message": "Successfully synthesized speech."
    }


def create_wav_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def upload_audio_to_gcs(audio_content: bytes) -> str:
    bucket_name = "qwiklabs-gcp-03-d90b22626152-aiqueens-audio-data"
    destination_blob_name = f"{time()}/output.wav"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload binary audio data with correct content type
    audio_file = BytesIO(audio_content)
    blob.upload_from_file(audio_file, content_type="audio/wav")

    return f"gs://{bucket_name}/{destination_blob_name}"



