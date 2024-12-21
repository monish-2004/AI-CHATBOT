import openai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_input):
    try:
        # Call OpenAI API to generate a response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"User: {user_input}\nAI:",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
