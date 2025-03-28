import abc
import typing as T
from pathlib import Path

import aiohttp
import pydantic as pdt
from tenacity import retry, stop_after_attempt

from footcrawl import metrics as metrics_
from footcrawl import parsers
from footcrawl.io import datasets, services

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
    metrics: metrics_.CrawlerMetrics = metrics_.CrawlerMetrics()

    @abc.abstractmethod
    async def crawl(self) -> Locals:
        """Run the crawler.

        Returns:
            Locals: Local crawler variables.
        """
        pass


class Engine(pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    logger_service: services.LoggerService = services.LoggerService()

    parser: parsers.ParserKind = pdt.Field(...)
    metrics: metrics_.CrawlerMetrics = pdt.Field(...)
    output: datasets.WriterKind = pdt.Field(...)

    def __init__(self, **data) -> None:
        super().__init__(**data)

        self._orig_path = self.output.path

    async def write_out(
        self, session: aiohttp.ClientSession, url: str, season: int
    ) -> None:
        logger = self.logger_service.logger()

        async for row in self._parse(session=session, url=url):
            # format output path
            formatted_path = self._orig_path.format(season=season)
            self.output.path = formatted_path

            logger.info("Writing to path: {}", self.output.path)
            await self.output.write(data=row)

    async def _parse(
        self, session: aiohttp.ClientSession, url: str
    ) -> T.AsyncGenerator[parsers.Item, None]:
        logger = self.logger_service.logger()

        resp = await self._fetch_content(session=session, url=url)

        async for item in self.parser.parse(response=resp):
            # Record items parsed
            self.metrics.record_parser(metrics={"items_parsed": 1})

            logger.debug("Parsed item: {}", item)
            yield item

    @retry(stop=stop_after_attempt(3))
    async def _fetch_content(
        self, session: aiohttp.ClientSession, url: str
    ) -> aiohttp.ClientResponse:
        resp = await session.get(url)
        resp.raise_for_status()

        # collecting metrics
        self.metrics.record_request(resp=resp)

        return resp

    def _check_filepaths(self, seasons: int) -> None:
        logger = self.logger_service.logger()

        for season in seasons:
            _output_path = self._orig_path.format(season=season)

            # remove the file before writing to it - don't want duplicates
            if Path(_output_path).absolute().exists():
                logger.info("Removing file: ", _output_path)
                Path(_output_path).absolute().unlink()

    @property
    def original_path(self) -> str:
        return self._orig_path
