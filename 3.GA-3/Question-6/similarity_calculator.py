import requests
import base64
import numpy as np

def calculate_similarity():
    # Get user inputs
    api_key = input("Enter your Jina API key: ")
    image_path = input("Enter the path to your image file: ")
    text = input("Enter the text description: ")
    
    # Read and encode the image
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return
    
    # Prepare the API request
    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "jina-clip-v2",
        "input": [
            {"text": text},
            {"image": encoded_image}
        ]
    }
    
    # Make the API request
    print("Sending request to Jina AI...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        # Extract embeddings
        text_embedding = np.array(data["data"][0]["embedding"])
        image_embedding = np.array(data["data"][1]["embedding"])
        
        # Calculate cosine similarity (dot product of normalized vectors)
        similarity = np.dot(text_embedding, image_embedding)
        
        print(f"\nSimilarity score: {similarity:.6f}")
        return similarity
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("AIrtGallery Similarity Calculator")
    print("================================")
    print("This program calculates the similarity between an image and text description")
    print("using Jina AI's CLIP V2 model.\n")
    
    print("Instructions:")
    print("1. You'll need a Jina AI API key (sign up at https://jina.ai/embeddings)")
    print("2. Prepare an image file (for this task: Tangram puzzle pieces)")
    print("3. Have a text description ready (for this task: 深度学习中的反向传播算法)\n")
    
    calculate_similarity() 