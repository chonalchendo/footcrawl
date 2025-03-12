import time

import httpx
import pydantic as pdt

from footcrawl import services


class Client(pdt.BaseModel, frozen=True, strict=True, extra="forbid"):
    user_agent: str
    download_delay: int = pdt.Field(default=1)
    follow_redirects: bool = pdt.Field(default=True)
    timeout: int = pdt.Field(default=20)
    proxy: str | None = pdt.Field(default=None)

    logger_service: services.LoggerService = services.LoggerService()

    def request(self, url: str) -> httpx.Response:
        logger = self.logger_service.logger()
        headers = self._get_headers()

        if self.download_delay > 0:
            logger.info(f"Delaying request for {self.download_delay} seconds")
            time.sleep(self.download_delay)

        logger.info("Sending request to {}", url)

        resq = httpx.get(
            url=url,
            headers=headers,
            follow_redirects=self.follow_redirects,
            proxy=self.proxy,
            timeout=self.timeout,
        )
        return resq

    def _get_headers(self) -> dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            # "Accept": "text/html,application/xhtml+xml,application/xml",
            # "Accept-Language": "en-US,en;q=0.9",
        }
