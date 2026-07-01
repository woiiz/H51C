from telegram import Update
from telegram.ext import ContextTypes
from app.keyboard import get_hosts_keyboard, get_host_details_keyboard
from app.crawler import fetch_live_hosts
from app.database import get_favorites, add_favorite, remove_favorite
from app.utils import restricted

@restricted
async def browse_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Fetching live hosts...")
    
    page = int(query.data.split("_")[-1])
    hosts = await fetch_live_hosts() # Optionally add pagination support to crawler
    
    if not hosts:
        await query.edit_message_text("No live hosts found right now.", reply_markup=get_hosts_keyboard(hosts))
        return
        
    await query.edit_message_text(
        text=f"<b>🌍 Live Hosts (Page {page+1})</b>\\nSelect a host to view details.",
        reply_markup=get_hosts_keyboard(hosts, page=page),
        parse_mode="HTML"
    )

@restricted
async def host_details_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    host_id = query.data.split("_")[1]
    hosts = await fetch_live_hosts()
    
    host = next((h for h in hosts if h['id'] == host_id), None)
    
    if not host:
        await query.edit_message_text("Host not found or went offline.")
        return
        
    favs = await get_favorites()
    is_fav = host_id in favs
    
    text = (
        f"<b>📺 Host Details</b>\\n\\n"
        f"👤 <b>Name:</b> {host['name']}\\n"
        f"🌍 <b>Country:</b> {host['country']}\\n"
        f"📊 <b>Status:</b> {host['status']}\\n"
        f"👁 <b>Viewers:</b> {host['viewers']}"
    )
    
    await query.edit_message_text(
        text=text,
        reply_markup=get_host_details_keyboard(host_id, is_favorite=is_fav),
        parse_mode="HTML"
    )

@restricted
async def toggle_favorite_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    host_id = query.data.split("_")[1]
    
    favs = await get_favorites()
    is_fav = host_id in favs
    
    if is_fav:
        await remove_favorite(host_id)
        await query.answer("Removed from favorites")
    else:
        await add_favorite(host_id)
        await query.answer("Added to favorites")
        
    # Refresh the host details view
    await host_details_callback(update, context)

@restricted
async def favorites_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Fetching favorites...")
    
    fav_ids = await get_favorites()
    if not fav_ids:
        await query.edit_message_text("You have no favorites yet.", reply_markup=get_hosts_keyboard([]))
        return
        
    hosts = await fetch_live_hosts()
    fav_hosts = [h for h in hosts if h['id'] in fav_ids]
    
    await query.edit_message_text(
        text="<b>⭐ Favorite Hosts</b>",
        reply_markup=get_hosts_keyboard(fav_hosts),
        parse_mode="HTML"
    )
