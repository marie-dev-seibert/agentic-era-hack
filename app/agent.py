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

from io import BytesIO
import os
import time
from google import genai
from google.genai import types

import google.auth
from google.adk.agents import Agent
from google.cloud import storage

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

genai_client = genai.Client()
storage_client = storage.Client()

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
        image_bucket_name = os.environ.get("IMAGE_BUCKET")

        response = genai_client.models.generate_images(
            model='imagen-4.0-generate-001', 
            prompt=prompt,
            config=types.GenerateImagesConfig()
        )

        image_bytes = response.generated_images[0].image.image_bytes

        image_buffer = BytesIO(image_bytes)

        blob_name = f"generated-images/{int(time.time())}.png"
        bucket = storage_client.bucket(image_bucket_name)
        blob = bucket.blob(blob_name)

        blob.upload_from_file(
            image_buffer,
            content_type='image/png'
        )

        public_url = f"https://storage.googleapis.com/{image_bucket_name}/{blob_name}"

        print(f"Success! Image URL: {public_url}")
        return f"Image generated! View it here: {public_url}"

    except Exception as e:
        print(f"An error occurred in generate_image: {e}")
        return f"An error occurred while generating the image: {e}"


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant designed to provide accurate and useful information.",
    tools=[generate_image],
)
