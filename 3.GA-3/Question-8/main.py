from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import httpx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Initialize FastAPI
app = FastAPI()

# Configuration - Set your token here
AIPROXY_TOKEN = "Replace with your Token"  # Replace this with the token you copied
EMBEDDING_URL = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"
EMBEDDING_MODEL = "text-embedding-3-small"

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request & Response Schemas
class SimilarityRequest(BaseModel):
    docs: List[str]
    query: str

class SimilarityResponse(BaseModel):
    matches: List[str]
    scores: List[float]

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            EMBEDDING_URL,
            headers={
                "Authorization": f"Bearer {AIPROXY_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "model": EMBEDDING_MODEL,
                "input": texts
            }
        )
        response.raise_for_status()
        data = response.json()
        return [item['embedding'] for item in data['data']]

@app.post("/similarity", response_model=SimilarityResponse)
async def get_similarity(request: SimilarityRequest):
    if not request.docs:
        raise HTTPException(status_code=400, detail="No documents provided")

    try:
        # Get embeddings for documents and query
        doc_embeddings = await get_embeddings(request.docs)
        query_embedding = await get_embeddings([request.query])
        
        # Calculate cosine similarities
        similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
        
        # Get top matches (up to 3 or number of docs, whichever is smaller)
        top_n = min(3, len(request.docs))
        top_indices = np.argsort(similarities)[-top_n:][::-1]  # Get top matches
        
        matches = [request.docs[i] for i in top_indices]
        scores = [float(similarities[i]) for i in top_indices]

        return SimilarityResponse(
            matches=matches,
            scores=scores
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Embedding service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Run server for local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8808)