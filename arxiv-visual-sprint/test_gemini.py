import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
api_base = os.environ.get("GEMINI_API_BASE")

client = genai.Client(api_key=api_key, http_options={"base_url": api_base})
try:
    response = client.models.generate_content(
        model="google/gemini-3.1-flash-image-preview",
        contents=["Hello"]
    )
    print("Success!", response.text)
except Exception as e:
    print("Error:", e)
