import requests
import json

# Variables
url = "https://aipipe.org/openai/v1/responses"
authorization_token = "AIPIPE TOKEN HERE"  # Replace with your actual token
input_data = "Input data from quesion" # Replace with your actual input data

# Headers and payload
headers = {
    "Authorization": authorization_token,
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-4.1-nano",
    "input": input_data
}

# POST request
response = requests.post(url, headers=headers, json=payload)

# Print the response
print(response.status_code)
data = response.json()
print("Input Tokens:", data["usage"]["input_tokens"])
