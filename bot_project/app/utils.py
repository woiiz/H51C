from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from app.config import OWNER_ID

def restricted(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != OWNER_ID:
            if update.message:
                await update.message.reply_text("Access Denied.")
            elif update.callback_query:
                await update.callback_query.answer("Access Denied.", show_alert=True)
            return
        return await func(update, context, *args, **kwargs)
    return wrapped
