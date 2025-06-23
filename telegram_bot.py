import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import uuid # For generating unique codes
import os

# Enable logging to see what your bot is doing
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# --- Bot Token Configuration ---
# It's best practice to load your bot token from environment variables
# For local testing, you can uncomment and set it directly, but for deployment,
# always use environment variables.
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7746373252:AAHNVeii20bX1wLBMTSPqMAUBbQyDXJeXcL')

if BOT_TOKEN == '7746373252:AAHNVeii20bX1wLBMTSPqMAUBbQyDXJeXcL':
    logger.warning("Using hardcoded bot token. Please set TELEGRAM_BOT_TOKEN environment variable in production.")

# --- Placeholder for a shared state/database ---
# In a real application, this would be a connection to a database (e.g., Firestore, PostgreSQL)
# that your Flask app also uses, to store and retrieve pending registration data.
# For this example, we'll use a simple dictionary to simulate it.
# Structure: {user_telegram_id: {"phone_number": "+1234567890", "code": "ABCDEF", "status": "pending"}}
# This needs to be persistent in a real app, not just in-memory.
# For demo purposes, we will imagine the Flask app sets an initial entry,
# and the bot then updates the code.
mock_database = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.full_name}) started the bot.")
    await update.message.reply_html(
        f"Hello {user.mention_html()}! 👋\n\n"
        "To register your Telegram account with our service, please first visit our website.\n"
        "Once you have entered your phone number on the website, come back here and type "
        "<b>/getcode</b> to receive your unique registration code.",
        # You might also include a direct link to your website's registration page here.
        # Example: "\n\n<a href='http://yourwebsite.com/register'>Go to our registration page</a>"
    )

async def get_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /getcode command.
    Generates a unique code and sends it to the user, associating it with their Telegram ID.
    In a real scenario, this would check a database for a pending registration from the website.
    """
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name
    logger.info(f"User {user_id} ({user_name}) requested a code with /getcode.")

    # --- Simulate checking for a pending registration from the website ---
    # In a real system, your Flask app would have stored a pending entry in a database
    # and possibly associated it with a temporary token that the bot can verify.
    # For this example, we'll just assume a pending state exists if not yet processed.

    # Check if this user has an entry in our mock database (meaning they started on the website)
    # This is a very simplified check. A robust system would link by a unique ID from the website.
    if user_id not in mock_database:
        # Simulate a new pending registration if it doesn't exist (for demo purposes)
        # In production, this means the user hasn't visited the website first.
        mock_database[user_id] = {"status": "awaiting_website_init", "phone_number": "unknown"}
        await update.message.reply_text(
            "It looks like you haven't started the registration on our website yet.\n"
            "Please go to our website first, enter your phone number, and then come back here to get your code."
        )
        return

    # Generate a unique 6-character alphanumeric code
    code = str(uuid.uuid4())[:6].upper()

    # Update the mock database with the generated code and the user's Telegram ID
    # This is the crucial step where the bot tells the "database" what code it gave out.
    mock_database[user_id]["code"] = code
    mock_database[user_id]["status"] = "code_generated"
    mock_database[user_id]["telegram_user_id"] = user_id # Store Telegram ID for verification

    logger.info(f"Generated code '{code}' for Telegram user {user_id}.")

    await update.message.reply_text(
        f"Your unique registration code is:\n\n`{code}`\n\n"
        "Please enter this code on our website to complete your registration.",
        parse_mode='MarkdownV2' # Use MarkdownV2 for monospace code block
    )
    # You might also prompt them to return to the website
    # Example: await update.message.reply_text("Click here to return to the website: http://yourwebsite.com/verify_code")

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes the user's message if it's not a command."""
    logger.info(f"Received message from {update.effective_user.id}: {update.message.text}")
    await update.message.reply_text(
        "I'm a registration bot. Please use the commands:\n"
        "/start - To begin\n"
        "/getcode - To get your registration code (after starting on the website)."
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("getcode", get_code_command))

    # Add handler for regular messages (non-commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    # Add error handler
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot started and polling for updates...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.full_name}) started the bot.")
    await update.message.reply_html(
        f"Hello {user.mention_html()}! 👋\n\n"
        "To register your Telegram account with our service, please first visit our website.\n"
        "Once you have entered your phone number on the website, come back here and type "
        "<b>/getcode</b> to receive your unique registration code."
    )
async def get_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /getcode command.
    Generates a unique code and sends it to the user, associating it with their Telegram ID.
    In a real scenario, this would check a database for a pending registration from the website.
    """
    user_id = update.effective_user.id
    # ... (simplified database lookup placeholder) ...

    # Generate a unique 6-character alphanumeric code
    code = str(uuid.uuid4())[:6].upper()

    # Update the mock database with the generated code and the user's Telegram ID
    # This is the crucial step where the bot tells the "database" what code it gave out.
    mock_database[user_id]["code"] = code
    mock_database[user_id]["status"] = "code_generated"
    mock_database[user_id]["telegram_user_id"] = user_id # Store Telegram ID for verification

    logger.info(f"Generated code '{code}' for Telegram user {user_id}.")

    await update.message.reply_text(
        f"Your unique registration code is:\n\n`{code}`\n\n"
        "Please enter this code on our website to complete your registration.",
        parse_mode='MarkdownV2'
    )
if __name__ == "__main__":
    main()
