from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

genai_client = genai.Client()

def generate_image(prompt: str, number_of_images: int = 1) -> str:
    """Generates images using the Imagen model based on a descriptive prompt.

    Args:
        prompt: The detailed text description of the image to generate.
        number_of_images: The number of images to create. Defaults to 1.

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
            model='imagen-3.0-generate-001', # Using a modern Imagen model
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=number_of_images,
            )
        )

        saved_files = []
        for i, generated_image in enumerate(response.generated_images):
            # Create a unique filename
            timestamp = int(time.time())
            filename = f"{prompt.replace(' ', '_')[:30]}_{timestamp}_{i}.png"
            filepath = os.path.join(output_dir, filename)

            # Save the image
            generated_image.image.save(filepath)
            saved_files.append(filepath)

        return f"Successfully generated {len(saved_files)} image(s) and saved them to: {', '.join(saved_files)}"

    except Exception as e:
        return f"An error occurred while generating the image: {e}"
