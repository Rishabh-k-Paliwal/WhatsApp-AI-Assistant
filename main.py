from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="WhatsApp AI Bot")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---- LLM function — test_groq.py se copy kiya ----
def ask_llm(user_message: str, system_prompt: str = None) -> str:
    if system_prompt is None:
        system_prompt = """You are a helpful WhatsApp assistant.
Keep replies under 100 words.
Reply in the same language as the user (Hindi/English/Hinglish)."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content

# ---- Health check endpoint ----
@app.get("/")
def root():
    return {"status": "Bot is running! 🤖"}

# ---- Main webhook — Twilio yahan call karega ----
@app.post("/webhook")
async def webhook(
    Body: str = Form(...),   # "..." matlab required field
    From: str = Form(...)    # sender number: "whatsapp:+91XXXXXXXXXX"
):
    user_message = Body
    sender = From
    
    print(f"\n📩 Message from {sender}")
    print(f"   Text: {user_message}")
    
    # LLM se reply lo
    reply = ask_llm(user_message)
    
    print(f"🤖 Reply: {reply}")
    
    # Abhi sirf return kar rahe hain
    # Module 4 mein Twilio se actual WhatsApp reply bhejenge
    return JSONResponse({
        "status": "ok",
        "received": user_message,
        "reply": reply
    })