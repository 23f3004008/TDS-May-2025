import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add session middleware for storing user info
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

# Configure OAuth client for Google
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.get("/")
async def home(request: Request):
    """
    Main route that handles:
    1. Initial redirect to Google login for unauthenticated users
    2. Processing the callback from Google authentication
    3. Displaying status for authenticated users
    """
    user = request.session.get("user")
    
    # For authenticated users, show success message
    if user:
        return {"message": "You are logged in", "email": user.get("email")}
    
    # For users who have just logged in, save their details in the session
    if "code" in request.query_params:
        token = await oauth.google.authorize_access_token(request)
        request.session["user"] = token.get("userinfo")
        request.session["id_token"] = token.get("id_token")
        return RedirectResponse("/")
    
    # For users who are logging in for the first time, redirect to Google login
    return await oauth.google.authorize_redirect(request, request.url)

@app.get("/id_token")
async def get_id_token(request: Request):
    """
    Return the ID token and client ID as JSON
    """
    id_token = request.session.get("id_token")
    if not id_token:
        return {"error": "Not authenticated. Please visit '/' to log in first."}
    
    return JSONResponse(content={
        "id_token": id_token,
        "client_id": os.getenv("GOOGLE_CLIENT_ID")
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True) 