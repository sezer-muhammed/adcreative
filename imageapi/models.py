# models.py for Task 1
from django.db import models

class ImageGeneration(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/', null=True, blank=True)
    color_hex = models.CharField(max_length=7)
    color_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Image Generation {self.id}"

# models.py for Task 2
class AdvertisementTemplate(models.Model):
    generated_image = models.ImageField(upload_to='generated_images/')
    logo = models.ImageField(upload_to='logos/')
    punchline = models.TextField()
    button_text = models.TextField()
    color_hex = models.CharField(max_length=7)
    advertisement_image = models.ImageField(upload_to='advertisements/', null=True, blank=True)

    def __str__(self):
        return f"Advertisement {self.id} - {self.punchline[:20]}"
