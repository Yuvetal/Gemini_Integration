import os
from dotenv import load_dotenv, dotenv_values
import google.generativeai as genai
from history_manager import append_to_history
from googlesearch import google_search

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Start a persistent chat session
model = genai.GenerativeModel("gemini-2.5-pro")
chat = model.start_chat()

# Define uncertainty indicators for confidence scoring
UNCERTAINTY_KEYWORDS = [
    "i'm not sure", "i don't know", "i cannot", "i can't", "as an ai", "i am unable",
    "i do not have access", "i don't have access", "i cannot provide", "i'm unable",
    "i'm sorry", "i apologize", "i don't have information", "i don't have data",
    "i don't have enough information", "i cannot verify", "i cannot confirm"
]

def compute_confidence_score(response_text):
    """
    Compute a confidence score based on the presence of uncertainty indicators.
    Score ranges from 0 (very uncertain) to 1 (very confident).
    """
    lowered = response_text.lower()
    penalty = sum(1 for keyword in UNCERTAINTY_KEYWORDS if keyword in lowered)
    score = max(0.0, 1.0 - (penalty * 0.1))  # Each keyword reduces confidence by 0.1
    return score

# Conversation loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = chat.send_message(user_input)
    gemini_reply = response.text
    confidence = compute_confidence_score(gemini_reply)

    if confidence < 0.6:
        print(f"Gemini is unsure (confidence score: {round(confidence, 2)}). Searching Google instead...")
        config = dotenv_values(".env")
        search_results = google_search(user_input, config["GOOGLE_API_KEY"], "a055bd0eb4fca45a3")

        if not search_results:
            print("No results found or an error occurred.")
            append_to_history(user_input, "Google Search returned no results.")
        else:
            formatted = ""
            for i, item in enumerate(search_results, start=1):
                formatted += f"\nResult {i}:\n{item['title']}\n{item['snippet']}\n{item['link']}\n"
            print(formatted)
            append_to_history(user_input, formatted)
    else:
        print("Gemini:", gemini_reply)
