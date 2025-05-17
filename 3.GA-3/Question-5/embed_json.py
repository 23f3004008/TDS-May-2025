import json

# Step 1: Define the input messages
message_1 = "First message"
message_2 = "Second message"

# Step 2: Prepare the JSON payload
payload = {
    "model": "text-embedding-3-small",
    "input": [message_1, message_2]
}

# Step 3: Print the JSON payload
print(json.dumps(payload, indent=2))
