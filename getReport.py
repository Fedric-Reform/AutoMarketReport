# getReport.py (This is the file Gunicorn expects: getReport:app)

import os
import logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Configuration ---
# The Gunicorn environment will automatically provide the BOT_TOKEN
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Command Handler Function ---

async def getfile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a PDF file in response to the /getfile command."""
    chat_id = update.effective_chat.id

    # Using the RAW link for reliable delivery:
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

# --- Webhook Application Setup ---

# 1. Initialize the Telegram Application (used to manage handlers)
# Use a simple function to build the application object
def build_application():
    """Builds and configures the Telegram Application."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set. Application cannot be built.")
        # Return a placeholder or raise an exception if the token is critical
        return None 
        
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("getfile", getfile_command))
    return application

# 2. Build the application instance
tg_application = build_application()

# 3. Initialize the Flask App (used to handle HTTP requests)
# This is the object Gunicorn looks for: 'app'
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
async def webhook_handler():
    """Handle incoming Telegram updates (POST) and simple GET requests."""
    
    if tg_application is None:
        # Emergency response if the application failed to initialize
        return jsonify({"status": "error", "message": "Bot application failed to initialize (Missing BOT_TOKEN?)."}), 500

    # Handle GET request (e.g., for health check)
    if request.method == "GET":
        return jsonify({"status": "running", "message": "Telegram Bot Webhook is online!"})
    
    # Handle POST request (Telegram update)
    if request.method == "POST":
        try:
            # 1. Get raw JSON data
            data = request.get_json(force=True)
            
            # 2. Convert to Telegram Update object
            update = Update.de_json(data, tg_application.bot)
            
            # 3. Process the update with the registered handlers
            # IMPORTANT: The Flask route is already 'async', which helps, 
            # but the entire process runs within Flask's asynchronous context.
            await tg_application.process_update(update)
            
            # 4. Success response
            return "ok" # Telegram must receive a 200 OK response
        
        except Exception as e:
            logger.error(f"Error processing webhook update: {e}")
            # Still return a 200 OK so Telegram doesn't retry endlessly
            return "ok"
