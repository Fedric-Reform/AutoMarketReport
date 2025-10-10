import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace with your actual Bot Token
BOT_TOKEN = "8441135029:AAHKCJDjq4LU5GuEZY25Mir4Y-On2xUmqgg" 

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Command Handler Function ---

async def getfile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a PDF file in response to the /getfile command."""
    chat_id = update.effective_chat.id

    # 1. Option: Send a PDF file from a public URL
    # Replace the URL with the direct link to your PDF file on GitHub or elsewhere.
    # Note: Telegram can usually handle files up to 50MB this way.
    # We'll use a placeholder URL here.

    pdf_url = "https://github.com/Fedric-Reform/AutoMarketReport/blob/main/Market%20Data%20Research.pdf" 
    
    # In a real-world scenario, you might get the raw content URL from a 
    # specific GitHub repository file link (e.g., raw.githubusercontent.com/...)

    await context.bot.send_message(chat_id, "Attempting to send the file from URL...")

    try:
        await context.bot.send_document(
            chat_id=chat_id,
            document=pdf_url,
            caption="Here is your requested PDF file (from URL).",
            filename="ReformDao Market Data Research.pdf" # Optional: set a custom filename
        )
        logger.info(f"PDF sent successfully from URL to chat {chat_id}")
    except Exception as e:
        logger.error(f"Error sending PDF from URL: {e}")
        await context.bot.send_message(chat_id, "Sorry, I couldn't send the PDF from the URL. Check the bot logs for details.")

    # 2. Option: Send a PDF file from a local file path
    # NOTE: For this to work, you must have a file named 'local_file.pdf' 
    # in the same directory as your bot script.
    
    local_file_path = "Market Data Research.pdf"
    
    if os.path.exists(local_file_path):
        await context.bot.send_message(chat_id, f"Attempting to send the file from local path: {local_file_path}...")
        try:
            with open(local_file_path, 'rb') as pdf_file:
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=pdf_file,
                    caption="Here is your requested PDF file (from local file).",
                    filename="Market Data Research.pdf" # Optional: set a custom filename
                )
            logger.info(f"PDF sent successfully from local file to chat {chat_id}")
        except Exception as e:
            logger.error(f"Error sending PDF from local file: {e}")
            await context.bot.send_message(chat_id, "Sorry, I couldn't send the local PDF file.")
    else:
        await context.bot.send_message(chat_id, f"Local PDF file '{local_file_path}' not found.")


# --- Main Bot Setup ---

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("getfile", getfile_command))

    # Start the Bot with polling
    print("Bot is running... Press Ctrl-C to stop.")
    application.run_polling(poll_interval=3.0)

if __name__ == "__main__":
    # IMPORTANT: Remember to replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token 
    # from BotFather before running.
    main()
