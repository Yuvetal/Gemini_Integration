import os
import json
import gzip
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")

# File path for compressed history
HISTORY_FILE = "conversation_history.json.gz"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with gzip.open(HISTORY_FILE, 'rt', encoding='utf-8') as f:
        return json.load(f)

def save_history(history):
    with gzip.open(HISTORY_FILE, 'wt', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

def summarize_history(history):
    messages = "\n".join([f"User: {entry['user']}\nGemini: {entry['gemini']}" for entry in history])
    prompt = f"Summarize the following conversation:\n\n{messages}"
    response = model.generate_content(prompt)
    summary = response.text
    return [{"summary": summary}]

def append_to_history(user_message, gemini_response):
    history = load_history()
    history.append({"user": user_message, "gemini": gemini_response})

    if len(history) >= 30:
        history = summarize_history(history)

    save_history(history)
