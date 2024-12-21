from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os
from flask_cors import CORS
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json

# Ensure necessary nltk resources are downloaded
nltk.download('punkt')
nltk.download('wordnet')


# Load environment variables from .env file
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the frontend

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents from JSON file
try:
    with open("intents.json") as file:
        intents = json.load(file)
except FileNotFoundError:
    print("Error: intents.json file not found.")
    intents = {"intents": []}  # Default empty intents

# Preprocess input by tokenizing and lemmatizing words
def preprocess_input(user_input):
    words = word_tokenize(user_input)
    words = [lemmatizer.lemmatize(w.lower()) for w in words]
    return words

# Match the user's input with defined intents
def match_intent(user_input, intents):
    words = preprocess_input(user_input)
    max_match = 0
    intent_response = None

    for intent in intents.get("intents", []):
        for pattern in intent.get("patterns", []):
            pattern_words = word_tokenize(pattern)
            match = len(set(words) & set(pattern_words)) / len(pattern_words)
            if match > max_match:
                max_match = match
                intent_response = intent.get("responses")

    if intent_response:
        return random.choice(intent_response)  # Return a random response from matched intent
    else:
        return "I'm sorry, I didn't understand that."

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles POST requests to the /chat endpoint.
    Sends user input to OpenAI API and returns the response.
    """
    try:
        # Get the user message from the request JSON
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"response": "Invalid input."}), 400

        # First, attempt to match intent using predefined patterns
        intent_response = match_intent(user_message, intents)
        
        # If no intent matches, use OpenAI to generate a response
        if intent_response == "I'm sorry, I didn't understand that.":
            response = openai.Completion.create(
                engine="text-davinci-003",  # OpenAI GPT model
                prompt=f"User: {user_message}\nAI:",
                max_tokens=150,
                temperature=0.7
            )
            bot_response = response.choices[0].text.strip()
        else:
            bot_response = intent_response

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    nltk.download('punkt')  # Download punkt tokenizer
    nltk.download('wordnet')  # Download wordnet lemmatizer data
    app.run(debug=True)
