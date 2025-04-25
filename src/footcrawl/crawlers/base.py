import abc
import typing as T

import aiohttp
import pydantic as pdt

from footcrawl import client, parsers, tasks
from footcrawl import metrics as metrics_
from footcrawl.io import datasets, files, services

type Locals = dict[str, T.Any]


class Crawler(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    """Base class for all crawlers.

    Attributes:
        url (str): URL to crawl.
        logger_service (services.LoggerService): Logger service.
        metrics (metrics.CrawlerMetrics): Metrics service.
        parser (parsers.ParserKind): Parser to use.
        output (datasets.WriterKind): Output writer to use.
        task_handler (tasks.TaskHandler): Task handler.
        file_handler (files.FileHandler): File handler.

    """

    KIND: str

    # base url
    url: str

    # services
    logger_service: services.LoggerService = services.LoggerService()

    # crawler parameters
    metrics: metrics_.CrawlerMetrics = metrics_.CrawlerMetrics()
    parser: parsers.ParserKind = pdt.Field(...)
    output: datasets.WriterKind = pdt.Field(..., discriminator="KIND")

    # handler parameters
    task_handler: tasks.TaskHandler = pdt.Field(..., default_factory=tasks.TaskHandler)
    file_handler: files.FileHandler = pdt.Field(..., default_factory=files.FileHandler)

    @abc.abstractmethod
    async def crawl(self) -> Locals:
        """Run the crawler.

        Returns:
            Locals: Local crawler variables.
        """
        pass

    async def _write_out(
        self,
        session: aiohttp.ClientSession,
        url: str,
        season: int,
        matchday: str | None = None,
    ) -> None:
        logger = self.logger_service.logger()

        async for item in self._parse(session=session, url=url):
            format_params = {"season": season}
            if matchday:
                format_params["matchday"] = matchday

            formatted_path = self.file_handler.format_original_path(**format_params)

            logger.info("Writing to path: {}", formatted_path)
            await self.output.write(output_path=formatted_path, data=item)

    async def _parse(
        self, session: aiohttp.ClientSession, url: str
    ) -> T.AsyncGenerator[parsers.Item, None]:
        logger = self.logger_service.logger()

        resp = await client.Response(url=url, session=session, metrics=self.metrics)()
        logger.debug("Parsing url: {}", resp.url)

        async for item in self.parser.parse(response=resp):
            logger.debug("Parsed item: {}", item)

            # Record items parsed
            self.metrics.record_parser(metrics={"items_parsed": 1})

            yield item

    def _format_url(self) -> str:
        raise NotImplementedError("Subclasses must implement _format_url method")
