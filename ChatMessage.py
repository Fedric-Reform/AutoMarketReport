import os
import requests

# Load environment variables set in the GitHub Workflow
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
REPORT_PATH = "Market Data Research.pdf"

if not all([BOT_TOKEN, CHAT_ID, REPORT_PATH]):
    print("Error: Missing environment variables (Token, Chat ID, or File Path).")
    exit(1)

# Construct the API URL for the sendDocument method
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

def send_pdf():
    """Sends the PDF file to the specified Telegram chat."""
    
    if not os.path.exists(REPORT_PATH):
        print(f"Error: File not found at path: {REPORT_PATH}")
        return

    print(f"Preparing to send file: {REPORT_PATH}")

    # Prepare the payload for the multipart/form-data request
    files = {
        'document': (REPORT_PATH, open(REPORT_PATH, 'rb')),
    }
    
    # Prepare the data part of the request
    data = {
        'chat_id': CHAT_ID,
        'caption': f"Hey, this is a very important update for you guys. I love cheese.",
    }

if __name__ == "__main__":
    send_pdf()
