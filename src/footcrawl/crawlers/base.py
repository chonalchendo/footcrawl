import abc
import typing as T

import pydantic as pdt

from footcrawl import metrics as metrics_
from footcrawl.io import services

type Locals = dict[str, T.Any]


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
    metrics: metrics_.CrawlerMetrics = metrics_.CrawlerMetrics()

    @abc.abstractmethod
    async def crawl(self) -> Locals:
        """Run the crawler.

        Returns:
            Locals: Local crawler variables.
        """
        pass
