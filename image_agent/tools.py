import os
import time
from google import genai
from google.genai import types
from io import BytesIO
from google.cloud import storage


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
            config=types.GenerateImagesConfig(
                aspect_ratio="1:1",
                output_mime_type="image/png",
            )
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