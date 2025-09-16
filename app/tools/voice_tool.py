from time import time
from typing import Dict, Any
from io import BytesIO
from google.cloud import texttospeech, storage
from google.adk.tools import ToolContext

def generate_voice(query: str, lang_code: str, voice_name: str) -> Dict[str, Any]:
    """Synthesizes speech from the input string of text or ssml.
    Make sure to be working in a virtual environment.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    Args:
        query: The text to convert to speech.
        tool_context: The ADK tool context for accessing runtime information.

    Returns:
        dict: Contains the synthesis result with status and audio information.
              - 'status' (str): "success" or "error".
              - 'audio_content' (bytes, optional): The synthesized audio data.
              - 'filename' (str, optional): The saved audio filename.
              - 'error_message' (str, optional): Description of error, if any.
    """

    try:
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(ssml=input)

        voice = texttospeech.VoiceSelectionParams(
            language_code="de-DE",  name="de-DE-Chirp3-HD-Charon",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config,
        )

        audio_url = upload_audio_to_gcs(response.audio_content)

        # Return the audio content and metadata
        return {
            "status": "success",
            "audio_url": audio_url,
            "message": "Successfully synthesized speech."
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to synthesize speech: {str(e)}"
        }


def upload_audio_to_gcs(audio_content: bytes) -> str:
    bucket_name = "qwiklabs-gcp-03-d90b22626152-aiqueens-audio-data"
    destination_blob_name = f"{time()}/output.mp3"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload binary audio data with correct content type
    audio_file = BytesIO(audio_content)
    blob.upload_from_file(audio_file, content_type="audio/mpeg")

    return f"gs://{bucket_name}/{destination_blob_name}"






def get_voices():
    """Lists the available voices."""
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")