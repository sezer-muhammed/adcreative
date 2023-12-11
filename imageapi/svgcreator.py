import cv2
from PIL import Image
import numpy as np

class SVGAdTemplateCreator:
    def __init__(self, ad_template):
        self.punchline = ad_template.punchline
        self.button_text = ad_template.button_text
        self.color_hex = ad_template.color_hex

        # Load the image using Pillow (PIL)
        generated_image_path = ad_template.generated_image.path
        try:
            pil_image = Image.open(generated_image_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found: {generated_image_path}")

        # Convert the Pillow image to OpenCV format
        self.image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Load the logo using Pillow (PIL)
        logo_path = ad_template.logo.path
        try:
            pil_logo = Image.open(logo_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Logo file not found: {logo_path}")

        # Convert the Pillow logo image to OpenCV format
        self.logo = cv2.cvtColor(np.array(pil_logo), cv2.COLOR_RGB2BGR)

    def create_ad(self):

        max_logo_size = 300
        logo_height, logo_width, _ = self.logo.shape
        if max(logo_height, logo_width) != max_logo_size:
            scale_factor = max_logo_size / max(logo_height, logo_width)
            self.logo = cv2.resize(self.logo, (int(logo_width * scale_factor), int(logo_height * scale_factor)))


        # Resize the image so that the max size is 1000
        max_image_size = 1000
        image_height, image_width, _ = self.image.shape
        if max(image_height, image_width) != max_image_size:
            scale_factor = max_image_size / max(image_height, image_width)
            self.image = cv2.resize(self.image, (int(image_width * scale_factor), int(image_height * scale_factor)))


        # Create a canvas of size 1080x1920 with a white background
        ad_canvas = np.zeros((1500, 1080, 3), dtype=np.uint8)
        ad_canvas.fill(255)  # Fill with white color

        # Calculate the position to place the logo
        logo_height, logo_width, _ = self.logo.shape
        logo_x = int((1080 - logo_width) / 2)
        logo_y = 40

        # Calculate the position to place the image
        image_height, image_width, _ = self.image.shape
        image_x = 40
        image_y = 340

        # Place the logo and image on the canvas
        ad_canvas[logo_y:logo_y + logo_height, logo_x:logo_x + logo_width] = self.logo
        ad_canvas[image_y:image_y + image_height, image_x:image_x + image_width] = self.image

        # Add a colored rectangle before the button text
        rectangle_color = tuple(int(self.color_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))  # Convert hex color to BGR
        rectangle_x = 0
        rectangle_y = image_y + image_height + 150
        rectangle_width = 1080
        rectangle_height = 100
        ad_canvas = cv2.rectangle(ad_canvas, (rectangle_x, rectangle_y), (rectangle_x + rectangle_width, rectangle_y + rectangle_height), rectangle_color, -1)

        # Center-align and colorize the punchline text
        punchline_font = cv2.FONT_HERSHEY_SIMPLEX
        punchline_font_scale = 1.5
        punchline_font_color = rectangle_color  # Use rectangle color for text
        punchline_thickness = 2
        punchline_text_size = cv2.getTextSize(self.punchline, punchline_font, punchline_font_scale, punchline_thickness)[0]
        punchline_x = int((1080 - punchline_text_size[0]) / 2)
        punchline_y = rectangle_y - 40
        cv2.putText(ad_canvas, self.punchline, (punchline_x, punchline_y), punchline_font, punchline_font_scale, punchline_font_color, punchline_thickness)

        # Add the button text below the rectangle
        button_font_scale = 1.5
        button_font_color = (255, 255, 255)  # White color for text
        button_text_size = cv2.getTextSize(self.button_text, punchline_font, button_font_scale, punchline_thickness)[0]
        button_x = int((1080 - button_text_size[0]) / 2)
        button_y = rectangle_y + int(rectangle_height / 2) + int(punchline_text_size[1] / 2)
        cv2.putText(ad_canvas, self.button_text, (button_x, button_y), punchline_font, button_font_scale, button_font_color, punchline_thickness)

        # Convert the OpenCV image to PIL format
        pil_ad_image = Image.fromarray(cv2.cvtColor(ad_canvas, cv2.COLOR_BGR2RGB))

        return pil_ad_image