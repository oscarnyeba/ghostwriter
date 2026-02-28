import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client (reads OPENAI_API_KEY from environment)
api_key = os.getenv("OPENAI_API_KEY", "dummy_key")
client = OpenAI(api_key=api_key)

PERSONAS = {
    "FOOTBALL": {
        "system_prompt": "You are a tactical expert in European Football, highly data-driven, analytical, and slightly controversial in your hot takes. You focus on player positioning, expected goals (xG), formations, and managerial decisions. Keep your tone engaging, sharp, and confident.",
        "topic": "European Football"
    },
    "TECH": {
        "system_prompt": "You are a product visionary and tech entrepreneur. You focus on real-world utility, user experience (UX), and the broader implications of consumer technology. Your tone is inspiring, forward-thinking, and pragmatic. Avoid buzzword-heavy fluff; focus on high-traffic 'hooks' and tangible value.",
        "topic": "Consumer Tech"
    }
}

def generate_tweets(niche_key, context_news, x_trends=None, num_tweets=2):
    """
    Generate insightful tweets based on the given news context using a specific persona.
    """
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
        print("OpenAI API Key not configured. Returning dummy text.")
        return f"[DUMMY TWEET 1 FOR {niche_key}]\n\n[DUMMY TWEET 2 FOR {niche_key}]"

    persona = PERSONAS.get(niche_key)
    if not persona:
        raise ValueError(f"Unknown niche: {niche_key}")

    prompt = (
        f"Based on the following recent news stories about {persona['topic']}:\n\n"
        f"{context_news}\n\n"
    )
    
    if x_trends:
        prompt += (
            f"Additionally, here are the current global trending topics on X (Twitter):\n"
            f"{x_trends}\n"
            f"If any of these trends naturally intersect with {persona['topic']}, feel free to reference them.\n\n"
        )

    prompt += (
        f"Write exactly {num_tweets} engaging, high-traffic Twitter posts (hooks) summarizing or opining on these developments. "
        "DO NOT sound like an AI summary. Sound like a native Twitter power user. "
        "Separate the tweets clearly with '----'."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": persona['system_prompt']},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating text from OpenAI: {e}")
        return f"Error generating tweets: {e}"

if __name__ == "__main__":
    # Test execution
    dummy_news = "Title: Real Madrid signs new midfielder for 100M euros.\nDescription: The tactical setup is expected to shift to a 4-3-3."
    tweets = generate_tweets("FOOTBALL", dummy_news)
    print("Football Tweets:\n", tweets)
