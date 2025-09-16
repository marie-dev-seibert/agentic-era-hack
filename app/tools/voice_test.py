from typing import Dict, Any
from google.cloud import texttospeech

def voice_test():
    """Synthesizes speech from the input string of text."""

    texts = [
        "Hey, ich bin wieder zurück! Willkommen, zum besten Content auf der Welt",
        "HEY! Ich bin wieder zurück! Willkommen, zum besten Content auf der Welt",
        "HEY! Ich bin wieder zurück, hier, beim besten Content auf der Welt",
        "HEY! Ich bin wieder zurück..., hier, beim besten Content auf der Welt",
        "HEY! Ich bin wieder zurück..., hier..., beim besten Content auf der Welt",
    ]
    client = texttospeech.TextToSpeechClient()


    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="de-DE",
        name="de-DE-Chirp3-HD-Achird",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    for text in texts:
        input_text = texttospeech.SynthesisInput(text=text)

        response = client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=audio_config,
        )

        # The response's audio_content is binary.
        with open(f"out/output_{text}.mp3", "wb") as out:
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')


if __name__ == "__main__":
    voice_test()