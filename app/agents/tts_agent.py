from google.adk.agents import Agent
from app.tools.tts_tool import tts_tool
from pydantic import BaseModel, Field

# TODO: Remove this
speaker_names = [
    "Alex",
    "Zoe",
]

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

tts_agent = Agent(
    name="tts_agent",
    model="gemini-2.5-flash",
    instruction=f"""
        You are a helpful AI assistant that generates text to speech for a podcast.

        1. User the {speaker_names} to find a matching voice name using this mapping: {VOICE_NAMES}
        2. Use the tts_tool to generate the audio with the speaker voice mapping

        Use the content and the tool tts_tool to generate the audio.
    """,
    description="Generates text to speech for a podcast.",
    tools=[tts_tool]
)
