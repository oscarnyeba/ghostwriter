import os
import argparse
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from scraper import get_trending_news, fetch_x_trends
from generator import generate_tweets
from notifier import send_whatsapp_message

# Load environment variables
load_dotenv()

def job():
    print(f"[{datetime.now()}] Starting AI Ghostwriter Job...")
    
    # 0. Fetch Global X Trends
    print("Fetching Global X Trends...")
    global_x_trends = fetch_x_trends()
    
    # 1. Scraping & Generation for Football
    print("Processing Football niche...")
    football_news = get_trending_news("European Football")
    football_tweets = generate_tweets("FOOTBALL", football_news, x_trends=global_x_trends, num_tweets=2)
    
    # 2. Scraping & Generation for Tech
    print("Processing Tech niche...")
    tech_news = get_trending_news("Consumer Tech")
    tech_tweets = generate_tweets("TECH", tech_news, x_trends=global_x_trends, num_tweets=2)
    
    # 3. Assemble message
    final_message = (
        "🤖 *AI Ghostwriter Daily Drafts*\n\n"
        "⚽ *Football Drafts* ⚽\n"
        f"{football_tweets}\n\n"
        "💻 *Tech Drafts* 💻\n"
        f"{tech_tweets}"
    )
    
    print("Drafts generated. Sending via WhatsApp...")
    # 4. Delivery
    success = send_whatsapp_message(final_message)
    if success:
        print("Job completed successfully. WhatsApp message sent.")
    else:
        print("Job completed, but WhatsApp delivery was skipped or failed. See output above.")

def main():
    parser = argparse.ArgumentParser(description="AI Ghostwriter Twitter/WhatsApp Application")
    parser.add_argument("--run-now", action="store_true", help="Run the pipeline immediately without scheduling")
    args = parser.parse_args()

    if args.run_now:
        print("Executing immediately as requested...")
        job()
        return

    # Scheduling mode
    schedule_time = os.getenv("SCHEDULE_TIME", "09:00")
    try:
        hour, minute = map(int, schedule_time.split(':'))
    except ValueError:
        print(f"Invalid SCHEDULE_TIME format: {schedule_time}. Defaulting to 09:00.")
        hour, minute = 9, 0

    print(f"Starting scheduler. Job configured to run daily at {hour:02d}:{minute:02d}.")
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour=hour, minute=minute)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()
