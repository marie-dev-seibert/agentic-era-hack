import os
import time
from google import genai
from google.adk.tools import ToolContext
from google.genai import types
from io import BytesIO
from google.cloud import storage
import google.auth

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


genai_client = genai.Client()
storage_client = storage.Client()

async def generate_image(prompt: str, tool_context: ToolContext) :
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
            config=types.GenerateImagesConfig(
                aspect_ratio="1:1",
                output_mime_type="image/png",
            )
        )

        image_bytes = response.generated_images[0].image.image_bytes

        image_buffer = BytesIO(image_bytes)

        blob_name = f"generated-image_{int(time.time())}.png"
        bucket = storage_client.bucket(image_bucket_name)
        blob = bucket.blob(blob_name)

        blob.upload_from_file(
            image_buffer,
            content_type='image/png'
        )

        public_url = f"https://storage.googleapis.com/{image_bucket_name}/{blob_name}"

        report_artifact = types.Part.from_bytes(
            data=image_bytes, mime_type="image/png"
        )

        await tool_context.save_artifact(blob_name, report_artifact)
        print(f"Image also saved as ADK artifact: {blob_name}")


        print(f"Success! Image URL: {public_url}")
        return {
            "status": "success",
            "message": f"Image generated .  ADK artifact: {blob_name}.",
            "artifact_name": blob_name,
        }

    except Exception as e:
        print(f"An error occurred in generate_image: {e}")
        return f"An error occurred while generating the image: {e}"