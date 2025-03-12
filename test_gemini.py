import google.generativeai as genai

# Configure API key
GEMINI_API_KEY = "AIzaSyBuUfZ4jQS73dwJ0_DQZIdws_0f3Nw8MaQ"
genai.configure(api_key=GEMINI_API_KEY)

try:
    # List available models
    print("Checking available models...")
    models = genai.list_models()
    for model in models:
        print(f"Found model: {model.name}")
    
    # Try to generate content
    print("\nTesting content generation...")
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content("Say hello!")
    print(f"Response: {response.text}")
    
    print("\nAPI test successful!")
    
except Exception as e:
    print(f"\nError testing API: {str(e)}")
    print("\nPlease make sure:")
    print("1. You have enabled the Generative Language API in Google Cloud Console")
    print("2. Your API key is correct")
    print("3. You have billing enabled in your Google Cloud project")
    print("4. You're in a region where Gemini API is available") 