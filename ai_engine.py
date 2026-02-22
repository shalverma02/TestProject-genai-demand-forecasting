import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from typing import List, Literal

from data_ingestion import fetch_live_trends
from database import setup_database, save_forecast

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
setup_database()

# 2. Advanced Output Architecture (Nested JSON Schema)
class TrendAnalysis(BaseModel):
    winning_category: str = Field(description="The specific product, raw material, or strategy mentioned in the news.")
    confidence_score: int = Field(description="Score from 1 to 10.")
    affected_materials: List[str] = Field(description="A list of 1 to 3 specific raw materials or components related to this trend (e.g., 'silicon', 'cotton', 'cardboard').")
    risk_level: Literal["Low", "Medium", "High", "Critical"] = Field(description="Assess the supply chain disruption risk.")
    strategic_recommendation: str = Field(description="A strict, one-sentence directive for the procurement team.")

# 3. Fetch Data
print("\nInitiating Advanced Demand Forecasting Pipeline...\n")
live_headlines = fetch_live_trends()

if not live_headlines:
    print("🚨 No live data found.")
    exit()

# 4. Advanced Prompt Engineering (Role, Context, Constraints)
prompt = f"""
ROLE: You are an elite Supply Chain Risk Analyst AI.
CONTEXT: You are analyzing live global retail and e-commerce news headlines.
DATA: 
{json.dumps(live_headlines, indent=2)}

TASK: 
1. Identify the most impactful supply chain trend from the data.
2. Deduce which underlying raw materials or physical components will see a surge in demand or face shortages based on this trend.
3. Classify the operational risk level.
4. Provide a single, actionable procurement directive.

CONSTRAINTS: Be highly specific. Do not use generic terms like 'goods'. Name actual materials.
"""

print("🧠 Brain activated. Running advanced schema extraction...\n")

# 5. AI Execution
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': TrendAnalysis,
        'temperature': 0.2 # Lower temperature forces the AI to be more analytical and less creative
    }
)

result = response.parsed

print("--- 🔮 ADVANCED FORECASTING RESULTS ---")
print(f"Target Trend:    {result.winning_category}")
print(f"Confidence:      {result.confidence_score}/10")
print(f"Risk Level:      {result.risk_level}")
print(f"Key Materials:   {', '.join(result.affected_materials)}")
print(f"Action required: {result.strategic_recommendation}\n")

# 6. Load Phase 
# (We are saving the category and appending the materials to the reasoning column to keep our DB simple for now)
db_reasoning = f"Risk: {result.risk_level} | Materials: {', '.join(result.affected_materials)} | Action: {result.strategic_recommendation}"
save_forecast(result.winning_category, result.confidence_score, db_reasoning)