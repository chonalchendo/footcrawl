import abc
import typing as T

import pydantic as pdt

from footcrawl import metrics
from footcrawl.io import services

Locals = dict[str, T.Any]


class Crawler(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    KIND: str

    url: str

    logger_service: services.LoggerService = services.LoggerService()
    crawler_metrics: metrics.CrawlerMetrics = metrics.CrawlerMetrics()

    @abc.abstractmethod
    async def crawl(self) -> Locals:
        pass
