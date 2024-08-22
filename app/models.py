# from pyrogram import Client, filters
import fal_client
import requests
import os

api = '8a3b414e-f7d8-47ae-84cc-29902ee6c375:b0b0e4c524651e961df4d9c19cd5d494'
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


def change_api(key):
    os.environ['FAL_KEY'] = key

    
def clarity_upscale(img):
    handler = fal_client.submit(
        "fal-ai/clarity-upscaler",
        arguments={
            "image_url": img
        },
    )
    return handler.request_id

def clarity_upscale_run(img):
    result = fal_client.run(
        "fal-ai/clarity-upscaler",
        arguments={
            "image_url": img
        },
    )
    # return handler.request_id
    return result['image']['url']


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


def credits(key):

    url = "https://rest.alpha.fal.ai/billing/user_balance"
    headers = {
        'Authorization': f'Key {key}',
    }

    try:
        # Make the GET request to the endpoint
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            return data
        else:
            print(f"Failed to retrieve credits: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {str(e)}")
        return None

 