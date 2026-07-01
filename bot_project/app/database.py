import aiosqlite
from app.config import DATABASE_PATH
import os

async def init_db():
    os.makedirs(os.dirname(DATABASE_PATH), exist_ok=True)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS Hosts (
                id INTEGER PRIMARY KEY,
                host_id TEXT UNIQUE,
                name TEXT,
                country TEXT,
                status TEXT,
                viewer_count INTEGER,
                thumbnail TEXT,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS Favorites (
                host_id TEXT PRIMARY KEY
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ExtractionHistory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host_id TEXT,
                url TEXT,
                status TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def get_favorites():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT host_id FROM Favorites") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def add_favorite(host_id: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO Favorites (host_id) VALUES (?)", (host_id,))
        await db.commit()

async def remove_favorite(host_id: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM Favorites WHERE host_id = ?", (host_id,))
        await db.commit()

async def log_extraction(host_id: str, url: str, status: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO ExtractionHistory (host_id, url, status) VALUES (?, ?, ?)",
            (host_id, url, status)
        )
        await db.commit()

async def get_recent_extracts(limit: int = 5):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT host_id, url, status, timestamp FROM ExtractionHistory ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ) as cursor:
            return await cursor.fetchall()
