import os
from google import genai
from google.genai import types
import wave
import google.auth

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), vertexai=False)

def voice_gemini(prompt: str, filename: str):

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker="Speaker01",
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name="Fenrir",
                                )
                            ),
                        ),
                        types.SpeakerVoiceConfig(
                            speaker="Speaker02",
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name="Enceladus",
                                )
                            ),
                        ),
                    ]
                )
            ),
        ),
    )

    data = response.candidates[0].content.parts[0].inline_data.data
    wave_file(filename, data)  # Saves the file to current directory

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

if __name__ == "__main__":
    prompts = [
        """TTS the following conversation between Speaker01 and Speaker02:
        Speaker01 very excited: Welcome Back! Let's start the show!
        Speaker02 bored: Yeah, let's start the show!
        """,
        """TTS the following song between Speaker01 and Speaker02:
        Speaker01 singing: Welcome Back! Let's start the show!
        Speaker02 humming: mmh! mmmmh! mmh! mmmmmmmmmmh!
        """,
        """TTS the following podcast between Speaker01 and Speaker02:
        Speaker01 doing an upbeat, whimsical intro music
        Speaker01 very excited: Welcome Back! Let's start the show!
        Speaker02 bored: Yeah, let's start the show!
        """,
    ]

    for i, prompt in enumerate(prompts):
        print(f"Generating voice for {prompt}")
        voice_gemini(prompt, f"out/output_{i}.wav")
