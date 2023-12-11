# admin.py
from django.utils.html import format_html
from django.contrib import admin
from .models import ImageGeneration, AdvertisementTemplate

class ImageGenerationAdmin(admin.ModelAdmin):
    list_display = ('id', 'color_hex', 'color_name', 'view_original_image', 'view_generated_image')
    readonly_fields = ('view_original_image', 'view_generated_image',)

    def view_original_image(self, obj):
        return self.get_image_html(obj.original_image)

    def view_generated_image(self, obj):
        return self.get_image_html(obj.processed_image)

    def get_image_html(self, image_field):
        if image_field:
            return format_html('<img src="{}" width="150" height="auto" />', image_field.url)
        return "-"

    view_original_image.short_description = "Original Image"
    view_generated_image.short_description = "Generated Image"

class AdvertisementTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'punchline', 'button_text', 'color_hex', 'view_logo', 'view_advertisement_image')
    readonly_fields = ('view_logo', 'view_advertisement_image',)

    def view_logo(self, obj):
        return self.get_file_html(obj.logo)

    def view_advertisement_image(self, obj):
        return self.get_file_html(obj.advertisement_image)  # Corrected field name

    def get_file_html(self, file_field):
        if file_field:
            return format_html('<a href="{}" target="_blank">View File</a>', file_field.url)
        return "-"

    view_logo.short_description = "Logo"
    view_advertisement_image.short_description = "Advertisement Image"

# Register your models here
admin.site.register(ImageGeneration, ImageGenerationAdmin)
admin.site.register(AdvertisementTemplate, AdvertisementTemplateAdmin)
