import asyncio
import typing as T

import pydantic as pdt

from footcrawl import client, parsers
from footcrawl.crawlers import base
from footcrawl.io import datasets


class AsyncClubsCrawler(base.Crawler):
    """Asynchronously crawl clubs data from a given URL.

    Attributes:
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

        logger.info("Initialising crawler engine")

        engine = base.Engine(
            parser=self.parser, metrics=self.metrics, output=self.output
        )

        logger.debug("Engine initialised: {}", engine)

        if engine.output.overwrite:
            logger.info("Overwrite is: {}", self.output.overwrite)
            engine._check_filepaths(seasons=self.seasons)

        async with self.http_client as client:
            session = client.get_session
            tasks = []

            for season in self.seasons:
                for league in self.leagues:
                    formatted_url = self.__format_url(league=league, season=season)

                    logger.debug(f"QUEUED: {formatted_url}")
                    task = asyncio.create_task(
                        engine.write_out(
                            session=session, url=formatted_url, season=season
                        )
                    )
                    tasks.append(task)

            await asyncio.gather(*tasks)

        metrics_output = engine.metrics.summary()
        logger.info("Crawler metrics: {}", metrics_output)

        return locals()  # returned for testing

    def __format_url(self, league: dict[str, str], season: int) -> str:
        return self.url.format(
            league=league.get("name"),
            league_id=league.get("id"),
            season=season,
        )
