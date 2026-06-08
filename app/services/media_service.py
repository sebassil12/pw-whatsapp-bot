import httpx

class MediaService:
    @staticmethod
    def download_bytes(media_url: str, account_sid: str, auth_token: str) -> bytes:
        response = httpx.get(media_url, auth=(account_sid, auth_token), timeout=30.0)
        response.raise_for_status()
        return response.content