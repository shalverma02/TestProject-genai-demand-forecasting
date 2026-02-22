import feedparser
import requests

def fetch_live_trends():
    print("📡 Fetching live data from Google News (Retail Trends)...")
    
    # The stable Google News RSS endpoint, specifically querying retail and ecommerce trends
    url = "https://news.google.com/rss/search?q=ecommerce+OR+retail+trends&hl=en-US&gl=US&ceid=US:en"
    
    # Our browser disguise
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"🚨 Connection failed! Status code: {response.status_code}")
        return []

    # Parse the raw XML into a clean Python list
    feed = feedparser.parse(response.content)
    
    trending_topics = []
    # Grab the top 5 headlines
    for entry in feed.entries[:5]:
        trending_topics.append(entry.title)
        
    return trending_topics

# --- ARCHITECT SAFETY CHECK ---
if __name__ == "__main__":
    live_data = fetch_live_trends()
    print("\n🔥 TOP 5 LIVE RETAIL TRENDS TODAY:")
    for i, trend in enumerate(live_data, 1):
        print(f"{i}. {trend}")