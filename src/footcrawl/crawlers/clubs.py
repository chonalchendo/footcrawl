import typing as T

import pydantic as pdt

from footcrawl import client, parsers
from footcrawl.crawlers import base


class AsyncClubsCrawler(base.Crawler):
    """Asynchronously crawl clubs data from a given URL.

    Attributes:
        seasons (list[int]): List of seasons to crawl.
        leagues (list[dict[str, str]]): List of leagues to crawl.
        parser (parsers.ClubsParser): Parser to parse the data.
        http_client (client.AsyncClient): HTTP client.
    """

    KIND: T.Literal["clubs"] = "clubs"

    # crawler parameters
    seasons: list[int]
    leagues: list[dict[str, str]]
    parser: parsers.ClubsParser = pdt.Field(default_factory=parsers.ClubsParser)

    # client
    http_client: client.AsyncClient

    @T.override
    async def crawl(self) -> base.Locals:
        logger = self.logger_service.logger()

        self.file_handler.set_original_path(path=self.output.base_path)

        if self.output.overwrite:
            self.file_handler.check_filepaths(seasons=self.seasons)

        async with self.http_client as client:
            session = client.get_session

            for season in self.seasons:
                for league in self.leagues:
                    self.task_handler.create_task(
                        self._write_out(
                            session=session,
                            season=season,
                            url=self._format_url(league=league, season=season),
                            file_handler=self.file_handler,
                        )
                    )

            await self.task_handler.gather_tasks()

        metrics_output = self.metrics.summary()
        logger.info("Crawler metrics: {}", metrics_output)

        return locals()  # returned for testing

    @T.override
    def _format_url(self, league: dict[str, str], season: int) -> str:
        return self.url.format(
            league=league.get("name"),
            league_id=league.get("id"),
            season=season,
        )
