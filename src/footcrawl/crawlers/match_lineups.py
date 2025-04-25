import typing as T

import polars as pl
import pydantic as pdt

from footcrawl import client, parsers
from footcrawl.crawlers import base
from footcrawl.io import datasets


class AsyncMatchLineupsCrawler(base.Crawler):
    KIND: T.Literal["match_lineups"]

    seasons: list[int]
    matchday: str
    parser: parsers.MatchLineupsParser = pdt.Field(
        default_factory=parsers.MatchLineupsParser
    )

    input: datasets.LoaderKind = pdt.Field(..., discriminator="KIND")

    http_client: client.AsyncClient = pdt.Field(default_factory=client.AsyncClient)

    @T.override
    async def crawl(self) -> base.Locals:
        logger = self.logger_service.logger()

        self.file_handler.set_original_path(path=self.output.base_path)

        if self.output.overwrite:
            self.file_handler.check_filepaths(seasons=self.seasons, matchday=self.matchday)

        async with self.http_client as client:
            session = client.get_session

            for season in self.seasons:
                fixtures = self.input.load(season=season)

                if self.matchday != "all":
                    fixtures = fixtures.filter(pl.col("matchday") == self.matchday)

                for fixture in fixtures.iter_rows(named=True):
                    self.task_handler.create_task(
                        self._write_out(
                            session=session,
                            season=season,
                            matchday=self.matchday,
                            url=self._format_url(
                                home_team=fixture["home_club_tm"],
                                away_team=fixture["away_club_tm"],
                                match_id=fixture["match_id"],
                            ),
                        )
                    )

            await self.task_handler.gather_tasks()

        metrics_output = self.metrics.summary()
        logger.info("Crawler metrics: {}", metrics_output)

        return locals()

    @T.override
    def _format_url(self, home_team: str, away_team: str, match_id: int) -> str:
        return self.url.format(
            home_team=home_team, away_team=away_team, match_id=match_id
        )
