import google.generativeai as genai

# TODO: Replace with your API key from Google AI Studio
genai.configure(api_key="AQ.Ab8RN6LtdFiSKvkeljkL5h1_yRQY-ek1oyaTZ_migoaRmM7Pfg")

model = genai.GenerativeModel('gemini-1.5-flash')

def test_connection():
    try:
        response = model.generate_content("Hello PocketSmart!")
        print("SUCCESS:", response.text)
        return True
    except Exception as e:
        print("ERROR:", e)
        return False

if __name__ == "__main__":
    test_connection()
