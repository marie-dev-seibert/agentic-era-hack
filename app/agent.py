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
import time
from google import genai
from google.genai import types

import google.auth
from google.adk.agents import Agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

genai_client = genai.Client()


def generate_image(prompt: str) -> str:
    """Generates images using the Imagen model based on a descriptive prompt.

    Args:
        prompt: The detailed text description of the image to generate.

    Returns:
        A string indicating success and the paths to the saved images, or an
        error message.
    """
    print(f"Tool 'generate_image' called with prompt: '{prompt}'")
    try:
        # Create a directory to save images if it doesn't exist
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)

        response = genai_client.models.generate_images(
            model='imagen-4.0-generate-001', 
            prompt=prompt,
            config=types.GenerateImagesConfig()
        )

        generated_image = response.generated_images[0]

        # Create a unique filename
        timestamp = int(time.time())
        filename = f"{prompt.replace(' ', '_')[:30]}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)

        # Save the image
        generated_image.image.save(filepath)

        return f"Successfully generated the image and saved it to: {filepath}"

    except Exception as e:
        return f"An error occurred while generating the image: {e}"


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant designed to provide accurate and useful information.",
    tools=[generate_image],
)
