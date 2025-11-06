import os
import requests
import sys

# Load environment variables (set via GitHub Secrets in the workflow)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# The message content (you can make this dynamic in the workflow)
MESSAGE_TEXT = os.environ.get("TELEGRAM_MESSAGE", "🤖 Automated message sent successfully via GitHub Actions!")

def send_telegram_message():
    """Constructs the API URL and sends a text message via Telegram's sendMessage method."""
    
    # 1. Validate environment variables
    if not all([BOT_TOKEN, CHAT_ID]):
        print("❌ Error: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables.")
        sys.exit(1)

    # 2. Construct API URL
    TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # 3. Prepare data payload
    data = {
        'chat_id': CHAT_ID,
        'text': MESSAGE_TEXT,
        'parse_mode': 'Markdown' # Optional: Allows you to format text with *bold* or _italics_
    }

    print(f"Preparing to send message to chat ID: {CHAT_ID}")
    
    # 4. Send the request
    try:
        response = requests.post(TELEGRAM_URL, data=data)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        result = response.json()
        if result.get('ok'):
            print(f"✅ Message successfully sent to Telegram: '{MESSAGE_TEXT}'")
        else:
            print(f"❌ Telegram API Error: {result.get('description', 'Unknown error')}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP/Network Error during sending: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_telegram_message()
