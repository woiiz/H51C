from telegram import Update
from telegram.ext import ContextTypes
from app.keyboard import get_extraction_result_keyboard
from app.extractor import extract_stream_url
from app.cache import get_cached_extraction, set_cached_extraction
from app.database import log_extraction, get_recent_extracts
from app.utils import restricted

@restricted
async def extract_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Extracting stream...")
    
    parts = query.data.split("_")
    host_id = parts[1]
    refresh = len(parts) > 2 and parts[2] == "refresh"
    
    result = None
    if not refresh:
        result = get_cached_extraction(host_id)
        
    if not result:
        result = await extract_stream_url(host_id)
        if result['status'] == 'SUCCESS':
            set_cached_extraction(host_id, result)
            
    await log_extraction(host_id, result.get('url', 'FAILED'), result['status'])
    
    if result['status'] == 'SUCCESS':
        text = (
            f"<b>✅ Extraction Successful</b>\\n\\n"
            f"👤 <b>Host ID:</b> {host_id}\\n"
            f"🌐 <b>CDN:</b> {result['cdn']}\\n\\n"
            f"🔗 <b>HLS URL:</b>\\n<code>{result['url']}</code>"
        )
        await query.edit_message_text(
            text=text,
            reply_markup=get_extraction_result_keyboard(host_id, result['url']),
            parse_mode="HTML"
        )
    else:
        text = f"<b>❌ Extraction Failed</b>\\n\\nError: {result.get('error', 'Unknown error')}"
        await query.edit_message_text(text=text, parse_mode="HTML")

@restricted
async def raw_request_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    host_id = query.data.split("_")[1]
    
    result = get_cached_extraction(host_id)
    if not result:
        await query.answer("Cache expired, please extract again.")
        return
        
    await query.answer()
    
    text = (
        f"<b>🔍 Raw Request Details</b>\\n\\n"
        f"<code>{result['raw_request']}</code>"
    )
    
    # We add a back button to the extraction result
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data=f"extract_{host_id}")]])
    
    await query.edit_message_text(text=text, reply_markup=kb, parse_mode="HTML")

@restricted
async def recent_extracts_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Loading recent extracts...")
    
    recent = await get_recent_extracts()
    if not recent:
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]])
        await query.edit_message_text("No recent extracts.", reply_markup=kb)
        return
        
    text = "<b>📄 Recent Extracts</b>\\n\\n"
    for host_id, url, status, timestamp in recent:
        status_emoji = "✅" if status == "SUCCESS" else "❌"
        # Truncate timestamp for display
        ts = str(timestamp).split(".")[0]
        text += f"{status_emoji} <b>Host:</b> {host_id} ({ts})\\n"
        
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="main_menu")]])
    await query.edit_message_text(text=text, reply_markup=kb, parse_mode="HTML")
