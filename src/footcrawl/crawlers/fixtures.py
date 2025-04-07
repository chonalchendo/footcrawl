import typing as T
import pydantic as pdt

from footcrawl import client, parsers
from footcrawl.crawlers import base
from footcrawl.io import datasets


class AsyncFixturesCrawler(base.Crawler):
    KIND: T.Literal["fixtures"] = "fixtures"

    # crawler parameters
    seasons: list[int]
    parser: parsers.FixturesParser = pdt.Field(default_factory=parsers.FixturesParser)

    # io parameters
    input: datasets.LoaderKind = pdt.Field(..., discriminator="KIND")

    # client
    http_client: client.AsyncClient = pdt.Field(default_factory=client.AsyncClient)

    @T.override
    async def crawl(self) -> base.Locals:
        logger = self.logger_service.logger()

        self.file_handler.set_original_path(path=self.output.base_path)

        if self.output.overwrite:
            self.file_handler.check_filepaths(seasons=self.seasons)

        async with self.http_client as client:
            session = client.get_session

            for season in self.seasons:
                clubs = self.input.load(season=season)
                
                for club in clubs:
                    name, club_id, league_id = (
                        club["tm_name"],
                        club["tm_id"],
                        club["league_id"],
                    )
                    self.task_handler.create_task(
                        self._write_out(
                            session=session,
                            season=season,
                            url=self._format_url(name, club_id, season, league_id),
                        )
                    )

            await self.task_handler.gather_tasks()

        metrics_output = self.metrics.summary()
        logger.info("Crawler metrics: {}", metrics_output)

        return locals()

    @T.override
    def _format_url(self, club: str, club_id: str, season: int, league_id: str) -> str:
        return self.url.format(
            club=club, club_id=club_id, season=season, league_id=league_id
        )
