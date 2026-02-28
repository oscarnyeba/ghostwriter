import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

def fetch_newsdata(query, num_results=3):
    """Fetch news from NewsData.io API."""
    if not NEWSDATA_API_KEY or NEWSDATA_API_KEY == "your_newsdata_api_key_here":
        print("NewsData API key not configured, falling back...")
        return None

    url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={requests.utils.quote(query)}&language=en"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success" and data.get("results"):
            articles = []
            for item in data["results"][:num_results]:
                title = item.get("title", "")
                description = item.get("description", "") or ""
                articles.append(f"Title: {title}\nDescription: {description}")
            return "\n\n".join(articles)
    except Exception as e:
        print(f"Error fetching from NewsData for {query}: {e}")
    
    return None

def fetch_google_news(query, num_results=3):
    """Fallback: Scrape Google News RSS feed."""
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll("item")
        
        articles = []
        for item in items[:num_results]:
            title = item.title.text
            # Description in RSS is usually HTML snippet, we extract just the text
            desc = BeautifulSoup(item.description.text, "html.parser").get_text()
            articles.append(f"Title: {title}\nDescription: {desc}")
            
        return "\n\n".join(articles)
    except Exception as e:
        print(f"Error fetching from Google News for {query}: {e}")
        return None

def get_trending_news(topic):
    """Get trending news for a given topic, using fallback if needed."""
    print(f"Fetching news for: {topic}")
    
    # Try NewsData API first
    news_text = fetch_newsdata(topic)
    
    if news_text:
        return news_text
        
    print("Falling back to Google News RSS...")
    # Fallback to Google News
    news_text = fetch_google_news(topic)
    
    if news_text:
        return news_text
        
    return "No trending news found at the moment."

def fetch_x_trends():
    """Fetch current X (Twitter) trends using Apify."""
    apify_api_key = os.getenv("APIFY_API_KEY")
    if not apify_api_key or apify_api_key == "your_apify_api_key_here":
        print("Apify API key not configured. Skipping X Trends.")
        return "X Trends unavailable."

    print("Fetching X Trends from Apify...")
    client = ApifyClient(apify_api_key)
    
    # We use a popular twitter trends scraper actor
    # Example: apidojo/tweet-scraper or easyapi/twitter-trending-topics-scraper
    run_input = {
        "startUrls": ["https://twitter.com/explore/tabs/trending"]
    }
    
    try:
        # EasyAPI Twitter Trending Topics Scraper
        actor_call = client.actor("easyapi/twitter-trending-topics-scraper").call()
        dataset_items = client.dataset(actor_call["defaultDatasetId"]).iterate_items()
        
        trends = []
        for i, item in enumerate(dataset_items):
            if i >= 10:  # Top 10
                break
            name = item.get("name", "")
            domain = item.get("domainContext", "")
            trends.append(f"{name} ({domain})")
            
        if trends:
            return ", ".join(trends)
        else:
            return "No trending topics found on X right now."
    except Exception as e:
        print(f"Error fetching X Trends: {e}")
        return "X Trends unavailable due to an error."

if __name__ == "__main__":
    # Test execution
    print(get_trending_news("European Football"))
    print("-" * 50)
    print(get_trending_news("Consumer Tech"))
