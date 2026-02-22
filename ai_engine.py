import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

# --- NEW: Import our Data Ingestion Module! ---
from data_ingestion import fetch_live_trends

# 1. Setup & Authentication
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Define Output Architecture
class TrendAnalysis(BaseModel):
    winning_category: str = Field(description="The single most promising retail category, product, or strategy based on the news")
    confidence_score: int = Field(description="Score from 1 to 10 indicating how strong this trend appears")
    reasoning: str = Field(description="A one-sentence explanation for why this category was chosen")

# 3. Fetch LIVE Data 📡
print("Initiating Demand Forecasting Pipeline...\n")
live_headlines = fetch_live_trends()

if not live_headlines:
    print("🚨 No live data found. Exiting pipeline.")
    exit()

# 4. The Prompt Payload 🧠
prompt = f"""
You are an AI Demand Forecasting Engine. 
Analyze the following live retail news headlines:
{json.dumps(live_headlines, indent=2)}

Based on these headlines, deduce the single most promising product category or retail strategy a supply chain manager should prepare for.
"""

print("\n🧠 Brain activated. Analyzing live data and formatting output...\n")

# 5. AI Execution
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': TrendAnalysis,
    }
)

result = response.parsed
print("--- 🔮 LIVE FORECASTING RESULTS ---")
print(f"Target Category: {result.winning_category}")
print(f"Confidence:      {result.confidence_score}/10")
print(f"Reason:          {result.reasoning}")