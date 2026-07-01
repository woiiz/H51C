from telegram import Update
from telegram.ext import ContextTypes
from app.keyboard import get_main_menu_keyboard
from app.utils import restricted

@restricted
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "<b>📺 HLS Live Explorer</b>\\n\\n"
        "Welcome to the production-ready live stream extractor.\\n"
        "Select an option below to begin."
    )
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )

@restricted
async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    welcome_text = (
        "<b>📺 HLS Live Explorer</b>\\n\\n"
        "Welcome to the production-ready live stream extractor.\\n"
        "Select an option below to begin."
    )
    await query.edit_message_text(
        text=welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )
