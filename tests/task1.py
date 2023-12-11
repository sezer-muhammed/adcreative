import requests
import os

# API endpoint URL
api_url = 'http://127.0.0.1:8000/imageapi/process-image/'  # Replace with your Django server URL

# Path to the image file
image_path = 'pexels-ray-piedra-1537671.jpg'  # Replace with the path to your image

# Color hex code
color_hex = '#000000'  # Example color hex code

# Check if the image file exists
if not os.path.exists(image_path):
    print(f"File not found: {image_path}")
    exit()

# Prepare the data for POST request
with open(image_path, 'rb') as image_file:
    files = {'image': (os.path.basename(image_path), image_file, 'image/jpg')}
    data = {'color_hex': color_hex}

    # Send POST request to the API
    response = requests.post(api_url, files=files, data=data)

    if response.status_code == 200:
        print("Image processed successfully.")
        print(response.json())
    else:

        print(response.text)
