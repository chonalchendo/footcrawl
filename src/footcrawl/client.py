import time

import httpx
import pydantic as pdt


class Client(pdt.BaseModel, frozen=True, strict=True, extra="forbid"):
    user_agent: str
    download_delay: int = pdt.Field(default=1)
    follow_redirects: bool = pdt.Field(default=True)
    proxy: dict | None = pdt.Field(default=None)

    def request(self, url: str) -> httpx.Response:
        if self.download_delay > 0:
            time.sleep(self.download_delay)

        headers = self._get_headers()
        resq = httpx.get(
            url=url,
            headers=headers,
            follow_redirects=self.follow_redirects,
            proxy=self.proxy,
        )
        return resq

    def _get_headers(self) -> dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml",
            "Accept-Language": "en-US,en;q=0.9",
        }
