# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import google.auth
from google.adk.agents import Agent
from app.agents.content_agent import content_agent
from app.agents.image_agent import image_agent
from app.agents.tts_agent import tts_agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="""
        You are an AI Agent that orchestrates routing to different agents.
        The workflow sequence is as follows:
        1. Content Agent to generate content
        2. Image Agent to generate image prompt based on the content
        3. TTS Agent to generate text to speech based on the content
    """,
    sub_agents=[
        content_agent,
        image_agent,
        tts_agent,
    ],
)