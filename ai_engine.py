import os
from dotenv import load_dotenv
from google import genai

# 1. Credential Management
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# --- ARCHITECT SAFETY CHECK ---
if not api_key:
    print("🚨 ERROR: Python cannot find your API key!")
    print("Please make sure your vault file is named exactly '.env' (no .txt) and contains no spaces around the equals sign.")
    exit()
else:
    print("✅ Key found! Connecting to the AI...\n")
# ------------------------------

# 2. Authentication & Instantiation (The Modern SDK Way)
client = genai.Client(api_key=api_key)

# 3. Execution
prompt = "You are a retail supply chain expert. In exactly one sentence, why is tracking social media trends useful for inventory forecasting?"

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

print(response.text)