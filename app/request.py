import requests
api = 'c57a1aa2-365a-4111-aa93-329b0658332c:122e40e0a920017aa9e4e1e326fd5fb8'

# Define the URL and headers
url = "https://fal.run/fal-ai/clarity-upscaler"
headers = {
    "Authorization": f"Key {api}",  # Replace YOUR_FAL_KEY with the actual key
    "Content-Type": "application/json"
}

# Define the data payload
data = {
    "image_url": "https://storage.googleapis.com/falserverless/gallery/NOCA_Mick-Thompson.resized.resized.jpg"
}

# Define the proxies
proxies = {
    "http": "fodev.org:8118",
}

# Make the POST request through the proxy
response = requests.post(url, headers=headers, json=data, proxies=proxies)

# Print the response
print(response.status_code)
print(response.json())
