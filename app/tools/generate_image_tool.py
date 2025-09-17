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
        response = genai_client.models.generate_images(
            model='imagen-4.0-generate-001', 
            prompt=prompt,
            config=types.GenerateImagesConfig(
                aspect_ratio="1:1",
                output_mime_type="image/png",
            )
        )

        image_bytes = response.generated_images[0].image.image_bytes

        artifact_name = f"generated-image_{int(time.time())}.png"

        save_image_in_bucket(tool_context, image_bytes, artifact_name)

        report_artifact = types.Part.from_bytes(
            data=image_bytes, mime_type="image/png"
        )

        await tool_context.save_artifact(artifact_name, report_artifact)

        return {
            "status": "success",
            "message": f"Image generated .  ADK artifact: {artifact_name}.",
            "artifact_name": artifact_name,
        }

    except Exception as e:
        print(f"An error occurred in generate_image: {e}")
        return f"An error occurred while generating the image: {e}"

def save_image_in_bucket(tool_context: ToolContext, image_bytes, filename: str):
    storage_client = storage.Client()
    image_bucket_name = os.environ.get("IMAGE_BUCKET")

    bucket = storage_client.bucket(image_bucket_name)
    blob = bucket.blob(filename)

    try:
        blob.upload_from_file(
            image_bytes,
            content_type='image/png'
        )

        gcs_uri = f"gs://{image_bucket_name}/{filename}"
        tool_context.state["generated_image_gcs_uri_" + filename] = gcs_uri

    except Exception as e_gcs:

        return {
            "status": "error",
            "message": f"Image generated but failed to upload to GCS: {e_gcs}",
        }