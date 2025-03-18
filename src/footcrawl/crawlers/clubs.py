import asyncio
import typing as T
from pathlib import Path

import aiohttp
import aiohttp.http_exceptions
import pydantic as pdt
from bs4 import BeautifulSoup

from footcrawl import parsers
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

    @T.override
    async def crawl(self) -> None:
        logger = self.logger_service.logger()

        self.__orig_output_path = self.output.path
        if self.output.overwrite:
            logger.info("Overwrite is: {}", self.output.overwrite)
            self.__check_filepaths()

        tasks = []
        for season in self.seasons:
            for league in self.leagues:
                _url = self.__format_url(league=league, season=season)

                logger.info(f"QUEUED: {_url}")
                task = asyncio.create_task(self.__parse(url=_url, season=season))
                tasks.append(task)

        await asyncio.gather(*tasks)

        metrics_output = self.crawler_metrics.summary()
        logger.info("Crawler metrics: {}", metrics_output)

    async def __parse(self, url: str, season: int) -> None:
        logger = self.logger_service.logger()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.error(f"Failed to fetch {url}, status: {resp.status}")
                    return None

                # record request metrics
                self.crawler_metrics.record_request(resp=resp)

                body = await resp.text()
                soup = BeautifulSoup(body, "html.parser")

                data = self.parser.parse(url=resp.url, soup=soup)
                logger.info("Parsed data: {}", data)

                # Record items parsed
                self.crawler_metrics.record_parser(metrics=self.parser.get_metrics)

                # format output path
                formatted_path = self.__orig_output_path.format(season=season)
                self.output.path = formatted_path

                logger.info("Writing to path: {}", self.output.path)
                await self.output.write(data=data)

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
