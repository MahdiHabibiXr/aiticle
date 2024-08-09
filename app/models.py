# from pyrogram import Client, filters
import fal_client
import requests
import os

api = 'c57a1aa2-365a-4111-aa93-329b0658332c:122e40e0a920017aa9e4e1e326fd5fb8'

os.environ['FAL_KEY'] = api

def upload(image_address):
    file = open(image_address, 'rb')
    file_bytes = file.read()

    file: bytes = file_bytes
    url = fal_client.upload(file, "image/jpeg")

    return url


def sdxl(prompt):
    result = fal_client.run(
        "fal-ai/fast-lightning-sdxl",
        arguments={
            "prompt": f'{prompt}',
        },
    )

    return result['images'][0]['url']


def swap(base, face):
    result = fal_client.run(
        "fal-ai/face-swap",
        arguments={
            "base_image_url": base,
            "swap_image_url": face
        },
    )

    return result

def tryon(person, garment, description, type):
    result = fal_client.run(
        "fal-ai/idm-vton",
        arguments={
            "human_image_url": person,
            "garment_image_url": garment,
            "description": description,
            "garment_type" : type
        },
    )

    export = [
        result['image']['url'],
        result['mask']['url']
    ]
    
    return export

def change_api(key):
    os.environ['FAL_KEY'] = api

#TODO: I should get the remaining credit of any api
#def get_credit(key):
    
def clarity_upscale(img):
    handler = fal_client.submit(
        "fal-ai/clarity-upscaler",
        arguments={
            "image_url": img
        },
    )
    return handler.request_id
    # return result['image']['url']


def tryon_sub():
    handler = fal_client.submit(
        "fal-ai/idm-vton",
        arguments={
            "human_image_url": "https://idm-vton.github.io/inthewild/4/h/0.jpeg",
            "garment_image_url": "https://idm-vton.github.io/inthewild/4/c2/c2.jpeg",
            "description": "Short Sleeve Round Neck T-shirts"
        },
    )

    return handler


def get_status(model_id, req_id):
    fal_key = api
    url = f'https://queue.fal.run/fal-ai/{model_id}/requests/{req_id}/status'
    headers = {
        'Authorization': f'Key {fal_key}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print('Success!')
        return response.json()
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        return response.text

def get_result(model_id, req_id):
    fal_key = api
    url = f'https://queue.fal.run/fal-ai/{model_id}/requests/{req_id}'
    headers = {
        'Authorization': f'Key {fal_key}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print('Success!')
        return response.json()
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        return response.text


