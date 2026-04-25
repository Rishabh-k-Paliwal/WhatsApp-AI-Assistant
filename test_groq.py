from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(user_message:str,system_prompt:str=None)->str:
    if system_prompt is None:
         system_prompt = "You are a sarcastic but helpful assistant who speaks in Hinglish."

    response = client.chat.completions.create(
         model="llama-3.1-8b-instant",
         messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": user_message}
         ],
         max_tokens=200,
         temperature=0.7
    )

    return response.choices[0].message.content

if __name__ == "__main__":
     test_message = [
        "Hello! Kya haal hai?",
        "Mujhe Python sikhna hai, kahan se shuru karun?",
        "What is RAG in AI?"
    ]
     
     for msg in test_message:
            print(f"User: {msg}")
            reply = ask_llm(msg)
            print(f" Bot: {reply}")
            print("-" * 50 )