import httpx
import logging
import time
from app.config import REQUEST_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)

async def fetch_live_hosts(country_code="ID", country_name="Indonesia", page=1):
    timestamp_ms = int(time.time() * 1000)
    url = "https://sw.fnccdn.com/501/api/plr/zbliv/public/live/h5/liveCenter.json"
    params = {
        "pageNum": page,
        "pageSize": 50,
        "area": country_code,
        "merchantId": "501",
        "lang": "ENU",
        "t": timestamp_ms
    }
    headers = {
        "User-Agent": USER_AGENT,
        "dev-type": "H5",
        "versioncode": "101",
        "Origin": "https://www.hot51.living",
        "Referer": "https://www.hot51.living/"
    }
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("code") not in [0, 200]:
                logger.warning(f"API returned non-success code: {data}")
            
            # Dynamically find the list of rooms in the JSON structure
            def find_rooms(obj):
                if isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, dict) and ('roomId' in item or 'memberId' in item or 'anchorId' in item):
                            return obj
                elif isinstance(obj, dict):
                    for k, v in obj.items():
                        res = find_rooms(v)
                        if res:
                            return res
                return []
                
            rooms = find_rooms(data)
            
            hosts = []
            for r in rooms:
                host_id = str(r.get('roomId') or r.get('memberId') or r.get('anchorId') or r.get('id', ''))
                if not host_id:
                    continue
                    
                name = r.get('nickname') or r.get('name') or r.get('anchorName') or f"Host_{host_id}"
                viewers = r.get('onlineCount') or r.get('viewers') or r.get('hot') or 0
                thumbnail = r.get('avatar') or r.get('cover') or r.get('pic') or ""
                
                # Capture stream URL
                stream_url = r.get('pullUrl') or r.get('streamUrl') or r.get('rtmpUrl') or r.get('hlsUrl')
                if not stream_url:
                    stream_info = r.get('stream', {}) or r.get('pull', {})
                    if isinstance(stream_info, str):
                        stream_url = stream_info
                    elif isinstance(stream_info, dict):
                        stream_url = stream_info.get('hls') or stream_info.get('flv') or stream_info.get('url')
                
                hosts.append({
                    "id": host_id,
                    "name": name,
                    "country": r.get('area') or country_name,
                    "status": "LIVE",
                    "viewers": viewers,
                    "thumbnail": thumbnail,
                    "stream_url": stream_url
                })
                
            if not hosts:
                logger.info(f"No hosts parsed. Raw response prefix: {str(data)[:500]}")
                
            return hosts
    except Exception as e:
        logger.error(f"Error fetching live hosts: {e}")
        return []

async def search_hosts(query: str):
    hosts = await fetch_live_hosts()
    return [h for h in hosts if query.lower() in h['name'].lower()]
