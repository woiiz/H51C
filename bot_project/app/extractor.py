import httpx
import logging
import re
from app.config import REQUEST_TIMEOUT, USER_AGENT
from app.crawler import fetch_live_hosts

logger = logging.getLogger(__name__)

async def extract_stream_url(host_id: str):
    """
    Extracts the .m3u8 URL for a given host_id.
    """
    try:
        hosts = await fetch_live_hosts()
        target_host = next((h for h in hosts if h['id'] == host_id), None)
        
        stream_url = None
        if target_host and target_host.get("stream_url"):
            stream_url = target_host["stream_url"]
            
        raw_request = f"GET /501/api/plr/zbliv/public/live/h5/liveCenter.json HTTP/1.1\\nHost: sw.fnccdn.com\\nUser-Agent: {USER_AGENT}\\ndev-type: H5\\nversioncode: 101"
        
        if not stream_url:
            return {
                "url": None,
                "error": "Stream URL not found in the liveCenter list. The host might be offline or the API structure changed.",
                "status": "FAILED"
            }
        
        # In case the URL is an .flv, some platforms support replacing it with .m3u8
        if stream_url.endswith('.flv'):
            stream_url = stream_url.replace('.flv', '.m3u8')
            
        cdn = "unknown"
        if "://" in stream_url:
            cdn = stream_url.split('/')[2]
            
        return {
            "url": stream_url,
            "cdn": cdn,
            "raw_request": raw_request,
            "status": "SUCCESS"
        }
    except Exception as e:
        logger.error(f"Extraction failed for {host_id}: {e}")
        return {
            "url": None,
            "error": str(e),
            "status": "FAILED"
        }
