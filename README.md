# AI Ghostwriter

An automated Python application that acts as an "AI Ghostwriter" for X (Twitter). It fetches trending topics in European Football and Consumer Tech, uses OpenAI GPT-4o to write engaging tweets under specific expert personas, and sends the drafts directly to your phone via WhatsApp.

## Features
- **Scraping**: Intelligently parses `newsdata.io` for target niches and falls back to Google News RSS feeds to ensure high availability.
- **X Trends**: Integrates `apify-client` to pull top real-time global trends directly from X to add context to the generated hooks.
- **AI Generation**: Employs engineered prompts for OpenAI's `gpt-4o` to emulate precise personas (e.g., Tactical Football Expert, Tech Visionary).
- **Delivery**: Automatically sends the formatted drafts to your designated WhatsApp number using Twilio.
- **Scheduling**: Includes a built-in scheduler (`APScheduler`) for daily execution or a manual override switch (`--run-now`) for immediate testing.

## Prerequisites
To run this application, you will need API keys and accounts for the following services:
- [OpenAI](https://platform.openai.com/)
- [NewsData.io](https://newsdata.io/)
- [Twilio](https://www.twilio.com/) (For WhatsApp delivery)
- [Apify](https://apify.com/) (For X Trends)

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/oscarnyeba/ghostwriter.git
   cd ghostwriter
   ```

2. **Install dependencies:**
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Copy the example environment file and fill in your credentials.
   ```bash
   cp .env.example .env
   ```
   *Note: Ensure `TARGET_WHATSAPP_NUMBER` is configured correctly (using the format `whatsapp:+[CountryCode][Number]`).*

4. **Test the Application:**
   Run the following command to execute the pipeline immediately and receive drafts on WhatsApp:
   ```bash
   python main.py --run-now
   ```

## Deployment
This repository includes a `Procfile` and `runtime.txt`, making it ready for deployment on platforms like Render, Railway, or PythonAnywhere.

### PythonAnywhere Deployment Example
1. Log into your PythonAnywhere Bash Console.
2. Clone this repository.
3. Create a virtual environment and install `requirements.txt`.
4. Create a `.env` file with your production API keys.
5. In the **Tasks** tab, configure a daily scheduled task pointing to the virtual environment and `main.py --run-now`.

## License
MIT License
