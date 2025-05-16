import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

TOKEN = "YOUR_BOT_TOKEN_HERE"  # 🔒 Replace with your actual token

# Define states
MENU = 0

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Persistent keyboard layout
persistent_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("Option 1", callback_data="option1")],
    [InlineKeyboardButton("Option 2", callback_data="option2")],
])

# Start command
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Welcome! Please choose an option:", reply_markup=persistent_menu
    )
    return MENU

# Button handler that keeps the menu alive
async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer(text=f"You selected {query.data.capitalize()}.", show_alert=False)
    await query.edit_message_reply_markup(reply_markup=persistent_menu)
    return MENU

# Cancel fallback (if you ever need it)
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

# Entry point
def main():
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .read_timeout(10)
        .write_timeout(10)
        .concurrent_updates(True)
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [CallbackQueryHandler(button)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
