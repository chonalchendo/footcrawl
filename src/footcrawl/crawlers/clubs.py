import asyncio
import typing as T
from pathlib import Path

import aiohttp
import aiohttp.http_exceptions
import pydantic as pdt
from bs4 import BeautifulSoup

from footcrawl import parsers, client
from footcrawl.crawlers import base
from footcrawl.io import datasets


class AsyncClubsCrawler(base.Crawler):
    KIND: T.Literal["AsyncClubsCrawler"] = "AsyncClubsCrawler"

    # crawler parameters
    seasons: list[int]
    leagues: list[dict[str, str]]
    parser: parsers.ClubsParser = parsers.ClubsParser()

    # io parameter
    output: datasets.WriterKind = pdt.Field(..., discriminator="KIND")

    # client
    http_client: client.AsyncClient = pdt.Field(...)

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

                    logger.info(f"QUEUED: {formatted_url}")
                    task = asyncio.create_task(
                        self.__write_out(
                            session=session, url=formatted_url, season=season
                        )
                    )
                    tasks.append(task)

            await asyncio.gather(*tasks)

        metrics_output = self.crawler_metrics.summary()
        logger.info("Crawler metrics: {}", metrics_output)
        
        return locals()   # returned for testing

    async def __write_out(
        self, session: aiohttp.ClientSession, url: str, season: int
    ) -> None:
        logger = self.logger_service.logger()
        data = await self.__parse(session=session, url=url)

        # format output path
        formatted_path = self.__orig_output_path.format(season=season)
        self.output.path = formatted_path

        logger.info("Writing to path: {}", self.output.path)
        await self.output.write(data=data)

    async def __parse(
        self, session: aiohttp.ClientSession, url: str
    ) -> dict[str, T.Any]:
        logger = self.logger_service.logger()

        body, resp = await self.__fetch_content(session=session, url=url)
        soup = BeautifulSoup(body, "html.parser")

        data = self.parser.parse(url=resp.url, soup=soup)
        logger.info("Parsed data: {}", data)

        # Record items parsed
        self.crawler_metrics.record_parser(metrics=self.parser.get_metrics)

        return data

    async def __fetch_content(
        self, session: aiohttp.ClientSession, url: str
    ) -> tuple[str, aiohttp.ClientResponse]:
        resp = await session.get(url)
        resp.raise_for_status()
        body = await resp.text()
        return body, resp

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
