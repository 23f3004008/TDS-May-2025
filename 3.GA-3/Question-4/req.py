import json

# Replace with your actual base64 image string
image_base64 = "Copied URL here"

# Prepare the JSON payload
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract text from this image."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"{image_base64}"}
                }
            ]
        }
    ]
}

# Print the JSON payload
print(json.dumps(payload, indent=2))
