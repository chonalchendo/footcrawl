import abc
import time
import typing as T
from collections import Counter

import pydantic as pdt

if T.TYPE_CHECKING:
    import aiohttp


type MetricsDict = dict[str, T.Any]


class Metrics(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    """A base class for metrics."""

    @abc.abstractmethod
    def summary(self) -> MetricsDict:
        """Return a summary of the metrics.

        Returns:
            MetricsDict: A dictionary of metrics.
        """
        pass


class CrawlerMetrics(Metrics):
    """A class for crawler metrics.

    Args:
        start_time (float): The start time of the crawler.
        total_requests (int): The total number of requests.
        successful_requests (int): The total number of successful requests.
        failed_requests (int): The total number of failed requests.
        parser_metrics (Counter): A counter for parser metrics.
    """

    start_time: float = time.time()
    total_requests: int = pdt.Field(default=0)
    successful_requests: int = pdt.Field(default=0)
    failed_requests: int = pdt.Field(default=0)
    parser_metrics: Counter = pdt.Field(default_factory=Counter)

    @T.override
    def summary(self) -> MetricsDict:
        return {
            "scraping_time": round(time.time() - self.start_time, 2),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.__calculate_request_success_rate(),
            "parser_metrics": dict(self.parser_metrics),
        }

    def record_request(self, resp: "aiohttp.ClientResponse") -> None:
        """Record a request.

        Args:
            resp (ClientResponse): The response object.
        """
        self.total_requests += 1

        if resp.status == 200:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

    def record_parser(self, metrics: MetricsDict) -> None:
        """Record parser metrics.

        Args:
            metrics (MetricsDict): The parser metrics.
        """
        if not isinstance(metrics, dict):
            raise ValueError("Metrics must be a dict class instance")

        self.parser_metrics.update(metrics)

    def __calculate_request_success_rate(self) -> float:
        """Calculate the request success rate."""
        if self.successful_requests > 0 and self.failed_requests == 0:
            return 100.0

        if self.total_requests == 0:
            return 0.0

        try:
            return round(self.successful_requests / self.total_requests, 2) * 100
        except ValueError as e:
            return e


class ParserMetrics(Metrics):
    """A class for parser metrics.

    Args:
        items_parsed (int): The total number of items parsed.
    """

    items_parsed: int

    @T.override
    def summary(self) -> MetricsDict:
        return {"items_parsed": self.items_parsed}
