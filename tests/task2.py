import requests

api_url = 'http://localhost:8000/imageapi/create-svg-ad/'
data = {
    'color_hex': '#FF00A0',
    'punchline': 'English Chars trouble of opencv',
    'button_text': 'English Chars'
}
files = {
    'main_image': open('pexels-i̇lkin-efendiyev-18221948.jpg', 'rb'),
    'logo_image': open('pexels-i̇lkin-efendiyev-18221948.jpg', 'rb')
}

response = requests.post(api_url, data=data, files=files)

if response.status_code == 200:
    print(response.text)
else:
    print("Failed to create SVG advertisement")
