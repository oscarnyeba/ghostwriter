import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp_message(content):
    """
    Send the generated drafts via WhatsApp using Twilio.
    """
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    to_number = os.getenv("TARGET_WHATSAPP_NUMBER")
    
    if not account_sid or account_sid == "your_twilio_sid_here":
        print("Twilio credentials not configured. Skipping WhatsApp delivery.")
        print(f"Drafts that would be sent:\n{content}")
        return False
        
    if not to_number or to_number == "whatsapp:+YOUR_NUMBER_HERE":
        print("Target WhatsApp number not configured. Skipping delivery.")
        return False

    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=content,
            from_=from_number,
            to=to_number
        )
        
        print(f"WhatsApp message sent successfully. SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending WhatsApp message via Twilio: {e}")
        return False

if __name__ == "__main__":
    # Test execution
    send_whatsapp_message("Hello from AI Ghostwriter!")
