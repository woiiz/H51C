import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from app.config import BOT_TOKEN, LOG_LEVEL
from app.database import init_db
from handlers.start import start_command, main_menu_callback
from handlers.browse import browse_callback, host_details_callback, toggle_favorite_callback, favorites_callback
from handlers.extract import extract_callback, raw_request_callback, recent_extracts_callback
import os

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set in .env")
        return
        
    application = Application.builder().token(BOT_TOKEN).build()

    # Setup Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    
    application.add_handler(CallbackQueryHandler(browse_callback, pattern="^browse_hosts_"))
    application.add_handler(CallbackQueryHandler(host_details_callback, pattern="^host_"))
    application.add_handler(CallbackQueryHandler(toggle_favorite_callback, pattern="^togglefav_"))
    application.add_handler(CallbackQueryHandler(favorites_callback, pattern="^favorites$"))
    
    application.add_handler(CallbackQueryHandler(extract_callback, pattern="^extract_"))
    application.add_handler(CallbackQueryHandler(raw_request_callback, pattern="^rawreq_"))
    application.add_handler(CallbackQueryHandler(recent_extracts_callback, pattern="^recent_extracts$"))
    
    # Ignore handler for unclickable buttons
    application.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.answer(), pattern="^ignore$"))

    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
    main()
