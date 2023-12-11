# serializers.py
from rest_framework import serializers
from .models import ImageGeneration, AdvertisementTemplate

class ImageGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGeneration
        fields = ['original_image', 'processed_image', 'color_hex', 'color_name']

class AdvertisementTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementTemplate
        fields = ['id', 'generated_image', 'logo', 'punchline', 'button_text', 'color_hex', 'advertisement_image']
