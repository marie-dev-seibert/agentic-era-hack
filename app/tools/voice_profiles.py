def synthesize_text_with_audio_profile():
    """Synthesizes speech from the input string of text for each effects profile."""
    from google.cloud import texttospeech
    import os

    text = "Hey, ich bin wieder zurück! Willkommen, zum besten Content auf der Welt"
    
    # List of all effects profile IDs to test
    effects_profile_ids = [
        "",  # No effects profile
        "wearable-class-device",
        "handset-class-device", 
        "headphone-class-device",
        "small-bluetooth-speaker-class-device",
        "medium-bluetooth-speaker-class-device",
        "large-home-entertainment-class-device",
        "large-automotive-class-device",
        "telephony-class-application"
    ]

    # Create output directory if it doesn't exist
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="de-DE",  name="de-DE-Chirp3-HD-Achird",
    )

    # Generate audio for each effects profile
    for effects_profile_id in effects_profile_ids:
        # Create filename based on effects profile
        if effects_profile_id == "":
            filename = "no-effects-profile.mp3"
        else:
            filename = f"{effects_profile_id}.mp3"
        
        output_path = os.path.join(output_dir, filename)
        
        # Note: you can pass in multiple effects_profile_id. They will be applied
        # in the same order they are provided.
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            effects_profile_id=[effects_profile_id] if effects_profile_id else [],
        )

        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{output_path}"')

if __name__ == "__main__":
    synthesize_text_with_audio_profile()
