import abc
import pydantic as pdt
import typing as T
import time
from collections import Counter

from aiohttp import ClientResponse


class Metrics(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    @abc.abstractmethod
    def summary(self) -> dict[str, T.Any]:
        pass


class CrawlerMetrics(Metrics):
    start_time: float = time.time()
    total_bytes_received: int = pdt.Field(default=0)
    total_requests: int = pdt.Field(default=0)
    successful_requests: int = pdt.Field(default=0)
    failed_requests: int = pdt.Field(default=0)
    parser_metrics: Counter = pdt.Field(default_factory=Counter)

    @T.override
    def summary(self) -> dict[str, T.Any]:
        return {
            "scraping_time": round(time.time() - self.start_time, 2),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.__calculate_request_success_rate(),
            "total_bytes_received": self.total_bytes_received,
            "parser_metrics": dict(self.parser_metrics),
        }

    def record_request(self, resp: ClientResponse) -> None:
        self.total_requests += 1

        content_length = int(resp.headers.get("Content-Length", 0))
        if resp.status == 200:
            self.successful_requests += 1
            self.total_bytes_received += content_length
        else:
            self.failed_requests += 1

    def record_parser(self, metrics: dict) -> None:
        if not isinstance(metrics, dict):
            raise ValueError("Metrics must be a dictionary class instance")

        self.parser_metrics.update(metrics)

    def __calculate_request_success_rate(self) -> float:
        if self.successful_requests > 1 and self.failed_requests == 0:
            return 100.0

        return round(self.total_requests / self.successful_requests, 2)


class ParserMetrics(Metrics):
    items_parsed: int
