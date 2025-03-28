import asyncio
import typing as T
from pathlib import Path

import aiohttp
import aiohttp.http_exceptions
import pydantic as pdt
from tenacity import retry, stop_after_attempt

from footcrawl import client, parsers
from footcrawl.crawlers import base
from footcrawl.io import datasets


class AsyncClubsCrawler(base.Crawler):
    """Asynchronously crawl clubs data from a given URL.

    Args:
        seasons (list[int]): List of seasons to crawl.
        leagues (list[dict[str, str]]): List of leagues to crawl.
        parser (parsers.ClubsParser): Parser to parse the data.
        output (datasets.WriterKind): Output writer.
        http_client (client.AsyncClient): HTTP client.
    """

    KIND: T.Literal["AsyncClubsCrawler"] = "AsyncClubsCrawler"

    # crawler parameters
    seasons: list[int]
    leagues: list[dict[str, str]]
    parser: parsers.ClubsParser = pdt.Field(default_factory=parsers.ClubsParser)

    # io parameter
    output: datasets.WriterKind = pdt.Field(..., discriminator="KIND")

    # client
    http_client: client.AsyncClient

    @T.override
    async def crawl(self) -> base.Locals:
        logger = self.logger_service.logger()

        self.__orig_output_path = self.output.path
        if self.output.overwrite:
            logger.info("Overwrite is: {}", self.output.overwrite)
            self.__check_filepaths()

        async with self.http_client as client:
            session = client.get_session
            tasks = []

            for season in self.seasons:
                for league in self.leagues:
                    formatted_url = self.__format_url(league=league, season=season)

                    logger.debug(f"QUEUED: {formatted_url}")
                    task = asyncio.create_task(
                        self.__write_out(
                            session=session, url=formatted_url, season=season
                        )
                    )
                    tasks.append(task)

            await asyncio.gather(*tasks)

        metrics_output = self.crawler_metrics.summary()
        logger.info("Crawler metrics: {}", metrics_output)

        return locals()  # returned for testing

    async def __write_out(
        self, session: aiohttp.ClientSession, url: str, season: int
    ) -> None:
        logger = self.logger_service.logger()

        async for row in self.__parse(session=session, url=url):
            # format output path
            formatted_path = self.__orig_output_path.format(season=season)
            self.output.path = formatted_path

            logger.info("Writing to path: {}", self.output.path)
            await self.output.write(data=row)

    async def __parse(
        self, session: aiohttp.ClientSession, url: str
    ) -> T.AsyncGenerator[parsers.Item, None]:
        logger = self.logger_service.logger()

        resp = await self.__fetch_content(session=session, url=url)

        async for item in self.parser.parse(response=resp):
            # Record items parsed
            parser_metrics = self.parser.get_metrics
            self.crawler_metrics.record_parser(metrics=parser_metrics)

            logger.debug("Parsed item: {}", item)
            yield item

    @retry(stop=stop_after_attempt(3))
    async def __fetch_content(
        self, session: aiohttp.ClientSession, url: str
    ) -> aiohttp.ClientResponse:
        resp = await session.get(url)
        resp.raise_for_status()

        # collecting metrics
        self.crawler_metrics.record_request(resp=resp)

        return resp

    def __format_url(self, league: dict[str, str], season: int) -> str:
        return self.url.format(
            league=league.get("name"),
            league_id=league.get("id"),
            season=season,
        )

    def __check_filepaths(self) -> None:
        logger = self.logger_service.logger()

        for season in self.seasons:
            _output_path = self.__orig_output_path.format(season=season)

            # remove the file before writing to it - don't want duplicates
            if Path(_output_path).absolute().exists():
                logger.info("Removing file: ", _output_path)
                Path(_output_path).absolute().unlink()
