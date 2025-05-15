import requests
from config import GEMINI_API_KEY

def get_gemini_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        try:
            return response_json['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError) as e:
            print(f"⚠️ Gemini Response Parsing Error: {e}")
            print("Full response:", response_json)
            return "Error: Unexpected response format from Gemini API."
    except Exception as e:
        print(f"⚠️ Gemini Error: {e}")
        print("Full response (if any):", response.text)
        return "Error: Failed to get a response from the Gemini API."


if __name__ == "__main__":
    print("🚀 Запускаем main.py")
    prompt = "Say hello in Fallout Pip-Boy style"
    result = get_gemini_response(prompt)
    print("🔮 Gemini says:", result)