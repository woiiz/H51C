from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📺 HLS Live Explorer", callback_data="ignore")],
        [InlineKeyboardButton("🌍 Browse Live Hosts", callback_data="browse_hosts_0")],
        [InlineKeyboardButton("🔍 Search Host", callback_data="search_host")],
        [InlineKeyboardButton("📄 Recent Extracts", callback_data="recent_extracts")],
        [InlineKeyboardButton("⭐ Favorites", callback_data="favorites")],
        [InlineKeyboardButton("⚙ Settings", callback_data="settings"),
         InlineKeyboardButton("ℹ About", callback_data="about")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_hosts_keyboard(hosts, page=0, per_page=5):
    keyboard = []
    start = page * per_page
    end = start + per_page
    
    for host in hosts[start:end]:
        keyboard.append([InlineKeyboardButton(f"🟢 {host['name']} ({host['viewers']} 👁)", callback_data=f"host_{host['id']}")])
    
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("← Prev", callback_data=f"browse_hosts_{page-1}"))
    if end < len(hosts):
        nav_row.append(InlineKeyboardButton("Next →", callback_data=f"browse_hosts_{page+1}"))
        
    if nav_row:
        keyboard.append(nav_row)
        
    keyboard.append([InlineKeyboardButton("Back to Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def get_host_details_keyboard(host_id, is_favorite=False):
    fav_text = "❌ Remove Favorite" if is_favorite else "⭐ Favorite"
    keyboard = [
        [InlineKeyboardButton("⚡ Extract Stream", callback_data=f"extract_{host_id}")],
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"host_{host_id}"),
         InlineKeyboardButton(fav_text, callback_data=f"togglefav_{host_id}")],
        [InlineKeyboardButton("Back", callback_data="browse_hosts_0")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_extraction_result_keyboard(host_id, url):
    keyboard = [
        [InlineKeyboardButton("📋 Copy URL", copy_text=url)],
        [InlineKeyboardButton("🔍 View Raw Request", callback_data=f"rawreq_{host_id}")],
        [InlineKeyboardButton("🔄 Refresh URL", callback_data=f"extract_{host_id}_refresh")],
        [InlineKeyboardButton("Back to Host", callback_data=f"host_{host_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)
