from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ImageGeneration, AdvertisementTemplate
from .serializers import ImageGenerationSerializer, AdvertisementTemplateSerializer  # Make sure you have this serializer
from .img2img_handler import ImageProcessor  # Import your ImageProcessor class
import requests
from PIL import Image
import io
from django.core.files.base import ContentFile
# views.py in your Django app
from rest_framework.response import Response
from .svgcreator import SVGAdTemplateCreator  # Import your SVGAdTemplateCreator class
import os
from django.core.files.base import ContentFile

def save_pil_image_to_imagefield(pil_image, obj):
    # Load your model instance based on the object_id

    # Convert the PIL Image to bytes
    image_bytes = io.BytesIO()
    pil_image.save(image_bytes, format='PNG')  # Adjust the format as needed (e.g., 'JPEG', 'PNG', etc.)

    # Create a ContentFile from the image bytes
    image_content = ContentFile(image_bytes.getvalue())

    # Assign the ContentFile to the ImageField
    obj.advertisement_image.save('output.png', image_content, save=True)  # Change the file name as needed

class ImageProcessView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        color_hex = request.data.get('color_hex')

        image = Image.open(image_file)

        # Get color name from external API
        color_name_response = requests.get(f"https://www.thecolorapi.com/id?hex={color_hex.lstrip('#')}")
        color_name = color_name_response.json()['name']['value'] if color_name_response.status_code == 200 else 'Unknown'

        processor = ImageProcessor()
        processed_image = processor.process_image(image, color_name)

        # Save the processed image to a ContentFile
        processed_image_io = io.BytesIO()
        processed_image.save(processed_image_io, format='PNG')
        processed_image_content = ContentFile(processed_image_io.getvalue())

        # Create an ImageGeneration instance
        image_instance = ImageGeneration(
            original_image=image_file,
            color_hex=color_hex,
            color_name=color_name
        )
        image_instance.processed_image.save(f"processed_{image_file.name}", processed_image_content)
        image_instance.save()

        # Use serializer to get the URL of the processed image
        serializer = ImageGenerationSerializer(image_instance)
        full_url = request.build_absolute_uri(image_instance.processed_image.url)

        return JsonResponse({'message': 'Image processed successfully', 'color_name': color_name, 'data': serializer.data, 'image_url': full_url})



class SVGAdCreationView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Extract image, logo, color, punchline, and button text from the request
        main_image_file = request.FILES.get('main_image')
        logo_image_file = request.FILES.get('logo_image')
        color_hex = request.data.get('color_hex')
        punchline = request.data.get('punchline')
        button_text = request.data.get('button_text')

        # Create an instance of AdvertisementTemplate
        ad_template = AdvertisementTemplate(
            generated_image=main_image_file,  # Assign if you have a generated image
            logo=logo_image_file,
            punchline=punchline,
            button_text=button_text,
            color_hex=color_hex
        )
        ad_template.save()


        svg_ad_creator = SVGAdTemplateCreator(
            ad_template
        )
        output_image = svg_ad_creator.create_ad()


        save_pil_image_to_imagefield(output_image, ad_template)
        full_image_url = request.build_absolute_uri(ad_template.advertisement_image.url)

        return Response({'message': 'Advertisement created successfully', 'advertisement_id':  AdvertisementTemplateSerializer(ad_template).data, 'image_url': full_image_url})
