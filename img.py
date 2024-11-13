import json
import time
import asyncio
import requests
import base64
from PIL import Image
from io import BytesIO


def base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

def send_img(image, text):

    bot_token = '6460907609:AAH0ZCfogSLjFUc0aVnS8ZO9McP7OF8DLek'
    chat_id = "-1001835144934"
    
    file = "img.png"

    files = {
        'photo': open(file, 'rb')
    }
    
    message = ('https://api.telegram.org/bot'+ bot_token + '/sendPhoto?chat_id=' + chat_id + "&caption=" + text)
    send = requests.post(message, files = files)
    
    
class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

def img(prompt):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '09A0E59E9D1CF456B5825ED7F4B85F7A', 'B19A7261728BDF9111D836D472C51CA2')
    model_id = api.get_model()
    uuid = api.generate(f"{prompt}", model_id)
    images = api.check_generation(uuid)
    image = base64_to_image(images[0])
    # image.show()  # Отобразить изображение
    image.save("img.png")
    send_img(image,prompt)
    
    
