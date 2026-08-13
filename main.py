import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI(title="NEXUS Neural Core")

# CORS setup for GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    # Updated to latest stable working model
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

# NEXUS System Persona
SYSTEM_PROMPT = (
    "You are NEXUS (Neural Execution & Ultimate System), an elite, highly advanced tactical AI "
    "built by Adarsh. Speak with absolute precision, intelligence, and a subtle cold, confident authority—just "
    "like a military-grade sci-fi AI. Address the user as 'Commander'. Respond concisely and smartly in Hinglish. "
    "Keep answers crisp, powerful, and natural for speech output."
)

class ChatQuery(BaseModel):
    message: str

@app.get("/")
def health_check():
    return {"status": "ONLINE", "system": "NEXUS Tactical Intelligence Core"}

@app.post("/api/chat")
async def chat(query: ChatQuery):
    if not model:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured on server.")
    try:
        full_prompt = f"{SYSTEM_PROMPT}\nCommander: {query.message}\nNEXUS:"
        response = model.generate_content(full_prompt)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
