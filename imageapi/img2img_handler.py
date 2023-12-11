import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from diffusers import StableDiffusionXLImg2ImgPipeline
import torch



class ImageProcessor:
    """
    A class for processing images using the BLIP model for captioning and Stable Diffusion XL for image enhancement.

    Methods
    -------
    process_image(init_image: PIL.Image, color: str) -> PIL.Image
        Processes the image by generating a caption and enhancing the image based on the specified color.
    """

    def __init__(self):
        """
        Initializes the ImageProcessor.
        """
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        self.refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        self.refiner.enable_model_cpu_offload()

    @staticmethod
    def resize_image(image, max_length=768) -> Image.Image:
        """
        Resizes the image maintaining the aspect ratio.

        Parameters
        ----------
        image : PIL.Image
            The image to resize.
        max_length : int, optional
            The maximum length for the longest dimension of the image.

        Returns
        -------
        PIL.Image
            The resized image.
        """
        ratio = max_length / max(image.size)
        new_size = tuple([int(x * ratio) for x in image.size])
        return image.resize(new_size, Image.Resampling.LANCZOS)

    def process_image(self, init_image: Image.Image, color: str) -> Image.Image:
        """
        Processes the image by generating a caption and enhancing the image based on the specified color.

        Parameters
        ----------
        init_image : PIL.Image
            The initial image to be processed.
        color : str
            The color to emphasize in the image enhancement.

        Returns
        -------
        PIL.Image
            The processed image.
        """
        resized_image = self.resize_image(init_image)
        inputs = self.processor(resized_image, return_tensors="pt")
        out = self.model.generate(max_length=40, min_length=15, **inputs)
        caption = self.processor.decode(out[0], skip_special_tokens=True)

        modified_caption = f"Create an image where the color {color} is heavily featured and prominently visible throughout the scene. {caption} The ambiance and mood of the image should be influenced by the color {color}, integrating {color} into the scene harmoniously."

        print(modified_caption)

        image = self.refiner(
            prompt=modified_caption, 
            image=resized_image, 
            strength=0.85,
            num_inference_steps=200
        ).images[0]

        return image

# Usage example
#raw_image = Image.open("pexels-i̇lkin-efendiyev-18221948.jpg").convert('RGB')
#processor = ImageProcessor()
#processed_image = processor.process_image(raw_image, "black")
#processed_image.show()