# HLS Live Explorer for Telegram

A production-ready Telegram bot to browse live hosts and extract playable HLS (`.m3u8`) stream URLs automatically.

## Features
- **Browse Live Hosts:** View paginated lists of currently live hosts.
- **Auto-Extraction:** One-tap automatic discovery of the stream CDN and playlist.
- **Caching:** Prevents spamming the target server by caching valid URLs.
- **Favorites & History:** Save favorite hosts and view recent extractions.
- **Async & Fast:** Built entirely on asynchronous I/O (`aiohttp`/`httpx`, `aiosqlite`, `python-telegram-bot`).
- **Secure:** Locked to `OWNER_ID`.

## Deployment on Ubuntu 24.04 LTS

1. **Clone the repository to `/opt/`**
   ```bash
   sudo mkdir -p /opt/hls-explorer
   # Copy the files into this directory
   cd /opt/hls-explorer
   ```

2. **Set up Virtual Environment**
   ```bash
   sudo apt update
   sudo apt install python3-venv python3-pip
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configuration**
   Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   nano .env
   ```
   *Make sure you set your Telegram Bot Token and your Telegram User ID (`OWNER_ID`).*

4. **Setup Systemd Service**
   ```bash
   sudo cp hls-explorer.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable hls-explorer
   sudo systemctl start hls-explorer
   ```

5. **View Logs**
   ```bash
   sudo journalctl -u hls-explorer -f
   ```

## Folder Structure Notes
The bot uses SQLite for storage in the `data/` directory and caches temporary extraction results in memory (and optionally in `cache/`).
