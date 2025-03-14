import asyncio
import time
import typing as T
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import aiohttp
import pydantic as pdt
from bs4 import BeautifulSoup
from yarl import URL

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

    # io parameter
    output: datasets.WriterKind = pdt.Field(..., discriminator="KIND")

    @T.override
    async def crawl(self) -> None:
        logger = self.logger_service.logger()
        start_time = time.time()

        self.__original_path = self.output.path
        if self.output.mode == "write":
            logger.info("Output mode: {}", self.output.mode)
            for season in self.seasons:
                _output_path = self.output.path.format(season=season)
                # remove the file before writing to it - don't want duplicates
                if Path(_output_path).absolute().exists():
                    logger.info("Removing file: ", _output_path)
                    Path(_output_path).absolute().unlink()

        tasks = []

        for season in self.seasons:
            for league in self.leagues:
                _url = self.url.format(
                    league=league.get("name"),
                    league_id=league.get("id"),
                    season=season,
                )
                logger.info(f"QUEUED: {_url}")
                task = asyncio.create_task(self.parse(url=_url))
                tasks.append(task)

        await asyncio.gather(*tasks)

        time_difference = time.time() - start_time
        logger.info("Scraping time: %.2f seconds." % time_difference)

    async def parse(self, url: str) -> None:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as resp:
                body = await resp.text()
                soup = BeautifulSoup(body, "html.parser")

                team_info = soup.find_all("td", {"class": "hauptlink no-border-links"})
                tm_team_name = [
                    td.find("a").get("href").split("/")[1] for td in team_info
                ]
                tm_team_id = [
                    td.find("a").get("href").split("/")[4] for td in team_info
                ]
                team_name = [td.find("a").get("title") for td in team_info]

                # get league and season from the url
                resp_url: URL = resp.url
                league = urlparse(str(resp_url)).path.split("/")[1]
                season = parse_qs(urlparse(str(resp_url)).query)["saison_id"][0]

                data = {
                    "league": league,
                    "season": season,
                    "tm_team_name": tm_team_name,
                    "tm_team_id": tm_team_id,
                    "team_name": team_name,
                }

                logger = self.logger_service.logger()

                logger.info("Parsed data: {}", data)

                # format output path
                formatted_path = self.__original_path.format(season=season)
                self.output.path = formatted_path

                logger.info("Writing to path: {}", self.output.path)
                await self.output.write(data=data)
