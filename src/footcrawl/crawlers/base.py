import abc

import pydantic as pdt

from footcrawl.io import services


class Crawler(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    KIND: str

    logger_service: services.LoggerService = services.LoggerService()

    @abc.abstractmethod
    async def crawl(self) -> None:
        pass
