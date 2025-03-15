import asyncio
import time
import typing as T
from pathlib import Path

import aiohttp
import pydantic as pdt
from bs4 import BeautifulSoup

from footcrawl import parsers
from footcrawl.crawlers import base
from footcrawl.io import datasets


class AsyncClubsCrawler(base.Crawler):
    KIND: T.Literal["AsyncClubsCrawler"] = "AsyncClubsCrawler"

    # network parameters
    url: str
    headers: dict[str, str]

    # crawler parameters
    seasons: list[int]
    leagues: list[dict[str, str]]
    parser: parsers.ClubsParser = parsers.ClubsParser()

    # io parameter
    output: datasets.WriterKind = pdt.Field(..., discriminator="KIND")

    @T.override
    async def crawl(self) -> None:
        logger = self.logger_service.logger()
        start_time = time.time()

        self.__orig_output_path = self.output.path

        if self.output.overwrite:
            logger.info("Overwrite is: {}", self.output.overwrite)
            self.__check_filepaths()

        tasks = []
        for season in self.seasons:
            for league in self.leagues:
                _url = self.url.format(
                    league=league.get("name"),
                    league_id=league.get("id"),
                    season=season,
                )
                logger.info(f"QUEUED: {_url}")
                task = asyncio.create_task(self.__parse(url=_url, season=season))
                tasks.append(task)

        await asyncio.gather(*tasks)

        time_difference = time.time() - start_time
        logger.info("Scraping time: %.2f seconds." % time_difference)

    async def __parse(self, url: str, season: int) -> None:
        logger = self.logger_service.logger()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.error(f"Failed to fetch {url}, status: {resp.status}")
                    return None

                body = await resp.text()
                soup = BeautifulSoup(body, "html.parser")

                data = self.parser.parse(url=resp.url, soup=soup)
                logger.info("Parsed data: {}", data)

                # format output path
                formatted_path = self.__orig_output_path.format(season=season)
                self.output.path = formatted_path

                logger.info("Writing to path: {}", self.output.path)
                await self.output.write(data=data)

    def __check_filepaths(self) -> None:
        logger = self.logger_service.logger()

        for season in self.seasons:
            _output_path = self.__orig_output_path.format(season=season)

            # remove the file before writing to it - don't want duplicates
            if Path(_output_path).absolute().exists():
                logger.info("Removing file: ", _output_path)
                Path(_output_path).absolute().unlink()
