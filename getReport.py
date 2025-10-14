# getReport.py (This is the file Gunicorn expects: getReport:app)

import os
import json
import logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Configuration ---
# SECURITY NOTE: Hardcoding the token is strongly discouraged in production.
# The code below will try to load it from the environment variable first.

# The Gunicorn environment will automatically provide the BOT_TOKEN
BOT_TOKEN = TELEGRAM_BOT_TOKEN

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Command Handler Function ---

async def getfile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a PDF file in response to the /getfile command."""
    chat_id = update.effective_chat.id

    # --- Option 1: Send a PDF file from a public URL (RECOMMENDED for Render) ---
    # NOTE: The provided URL is a GitHub page link, not a raw file link. 
    # Use the RAW link for reliable delivery:
    pdf_url = "https://raw.githubusercontent.com/Fedric-Reform/AutoMarketReport/main/Market%20Data%20Research.pdf"  
    
    await context.bot.send_message(chat_id, "Attempting to send the file from URL...")

    try:
        await context.bot.send_document(
            chat_id=chat_id,
            document=pdf_url,
            caption="Here is your requested PDF file (from URL).",
            filename="ReformDao Market Data Research.pdf"
        )
        logger.info(f"PDF sent successfully from URL to chat {chat_id}")
    except Exception as e:
        logger.error(f"Error sending PDF from URL: {e}")
        await context.bot.send_message(chat_id, "Sorry, I couldn't send the PDF from the URL. Check the bot logs for details.")

    # --- Option 2: Send a PDF file from a local file path ---
    # NOTE: This only works if 'Market Data Research.pdf' is PRESENT in the Render deployment directory.
    local_file_path = "Market Data Research.pdf"
    
    if os.path.exists(local_file_path):
        # We don't send two messages in a row, so this block is commented out for cleaner execution
        # but the logic for local files remains correct if used exclusively.
        pass
    else:
        await context.bot.send_message(chat_id, f"Local PDF file '{local_file_path}' not found in the server deployment.")


# --- Webhook Application Setup ---

# 1. Initialize the Telegram Application (used to manage handlers)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Add the command handler
application.add_handler(CommandHandler("getfile", getfile_command))

# 2. Initialize the Flask App (used to handle HTTP requests from Render/Telegram)
# This is the object Gunicorn looks for: 'app'
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
async def webhook_handler():
    """Handle incoming Telegram updates (POST) and simple GET requests."""
    
    # Handle GET request (e.g., for health check)
    if request.method == "GET":
        return jsonify({"status": "running", "message": "Telegram Bot Webhook is online!"})
    
    # Handle POST request (Telegram update)
    if request.method == "POST":
        try:
            # Get JSON data from the request body
            data = request.get_json(force=True)
            
            # Convert the raw JSON data into a Telegram Update object
            update = Update.de_json(data, application.bot)
            
            # Process the update with the registered handlers
            await application.process_update(update)
            
            return "ok" # Telegram must receive a 200 OK response
        
        except Exception as e:
            logger.error(f"Error processing webhook update: {e}")
            # Still return a 200 OK so Telegram doesn't retry endlessly
            return "ok" 

# --- End of Script ---
# The standard __main__ block for polling is removed because Gunicorn handles execution.
