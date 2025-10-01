import os
import requests

# Load environment variables set in the GitHub Workflow
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
REPORT_PATH = os.environ.get("Market Data Research.pdf")

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
        'caption': f"📊 Weekly Report: {os.path.basename(REPORT_PATH)}",
    }

    try:
        response = requests.post(TELEGRAM_URL, data=data, files=files)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Check Telegram's response status
        if response.json().get("ok"):
            print("Successfully sent PDF report to Telegram.")
        else:
            print(f"Telegram API Error: {response.json().get('description', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Important: Close the file handle after sending
        files['document'][1].close()

if __name__ == "__main__":
    send_pdf()
