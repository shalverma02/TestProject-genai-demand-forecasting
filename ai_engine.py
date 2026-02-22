import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

# 1. Setup & Authentication
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Define the Output Architecture (The Blueprint)
# This forces the AI to return exactly this data structure, nothing else.
class TrendAnalysis(BaseModel):
    winning_product: str = Field(description="The name of the single best product")
    impulse_buy_score: int = Field(description="Score from 1 to 10")
    reasoning: str = Field(description="A one-sentence explanation for the score")

# 3. Mock Data Input (Simulating a Pinterest API pull)
pinterest_trends = {
    "platform": "Pinterest",
    "target_audience": "Gen Z & Millennials",
    "trending_search_terms": ["chunky knit blankets", "mushroom lamp", "matcha whisk set"],
    "growth_velocity": "High"
}

# 4. The Prompt Payload
prompt = f"""
You are an AI Demand Forecasting Engine. 
Analyze the following social media trend data:
{json.dumps(pinterest_trends, indent=2)}

Evaluate these trends and identify the single item with the highest 'Impulse Buy Potential'.
"""

print("Analyzing trends and forcing structured JSON output...\n")

# 5. Execution
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': TrendAnalysis,
    }
)

# Because we used Pydantic, the SDK automatically parses the JSON back into Python variables!
result = response.parsed
print("--- FORECASTING RESULTS ---")
print(f"Product: {result.winning_product}")
print(f"Score:   {result.impulse_buy_score}/10")
print(f"Reason:  {result.reasoning}")