import abc
import typing as T

import pydantic as pdt

from footcrawl import metrics
from footcrawl.io import services

Locals = dict[str, T.Any]


class Crawler(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    """Base class for all crawlers.

    Args:
        url (str): URL to crawl.
        logger_service (services.LoggerService): Logger service.
        crawler_metrics (metrics.CrawlerMetrics): Metrics service.
    """

    KIND: str

    url: str

    logger_service: services.LoggerService = services.LoggerService()
    crawler_metrics: metrics.CrawlerMetrics = metrics.CrawlerMetrics()

    @abc.abstractmethod
    async def crawl(self) -> Locals:
        """Run the crawler.

        Returns:
            Locals: Local crawler variables.
        """
        pass
