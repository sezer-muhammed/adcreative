# urls.py in your Django app

from django.urls import path
from .views import ImageProcessView, SVGAdCreationView

urlpatterns = [
    path('process-image/', ImageProcessView.as_view(), name='process_image'),
    path('create-svg-ad/', SVGAdCreationView.as_view(), name='create_svg_ad'),
]
