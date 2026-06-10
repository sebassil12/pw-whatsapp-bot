import httpx

class MediaService:
    @staticmethod
    def download_bytes(media_url: str, account_sid: str, auth_token: str) -> tuple[bytes, str | None]:
        response = httpx.get(
            media_url,
            auth=(account_sid, auth_token),
            timeout=30.0,
            follow_redirects=True,
        )
        response.raise_for_status()
        return response.content, response.headers.get("content-type")