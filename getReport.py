import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIGURATION ---
BOT_TOKEN = os.get"YOUR_BOT_TOKEN_HERE"
ADMIN_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Example GitHub raw file link
GITHUB_FILE_URL = "https://raw.githubusercontent.com/Fedric-Reform/AutoMarketReport/main/Market%20Data%20Research.pdf"

# --- LOGGING SETUP ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- EXISTING COMMAND (still works) ---
async def getfile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    pdf_url = "https://github.com/Fedric-Reform/AutoMarketReport/blob/main/Market%20Data%20Research.pdf"

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
        await context.bot.send_message(chat_id, "Sorry, I couldn't send the PDF from the URL.")


# --- NEW COMMAND: send file from GitHub (admin only) ---
async def githubfile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if user_id != ADMIN_ID:
        await context.bot.send_message(chat_id, "⛔ You are not authorized to use this command.")
        return

    await context.bot.send_message(chat_id, "📡 Fetching latest file from GitHub...")

    try:
        # Download file from GitHub raw link
        response = requests.get(GITHUB_FILE_URL)
        response.raise_for_status()

        # Send file
        await context.bot.send_document(
            chat_id=chat_id,
            document=response.content,
            filename=os.path.basename(GITHUB_FILE_URL),
            caption="✅ Latest file fetched from GitHub."
        )
        logger.info(f"✅ File sent successfully to admin {user_id}")

    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub file fetch failed: {e}")
        await context.bot.send_message(chat_id, "❌ Failed to fetch file from GitHub.")


# --- MAIN BOT SETUP ---
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Register commands
    application.add_handler(CommandHandler("getfile", getfile_command))
    application.add_handler(CommandHandler("githubfile", githubfile_command))

    print("🤖 Bot is running... Press Ctrl-C to stop.")
    application.run_polling(poll_interval=3.0)


if __name__ == "__main__":
    main()
