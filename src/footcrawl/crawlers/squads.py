import typing as T

import pydantic as pdt

from footcrawl import client, parsers
from footcrawl.crawlers import base
from footcrawl.io import datasets


class AsyncSquadsCrawler(base.Crawler):
    KIND: T.Literal["squads"] = "squads"

    # crawler parameters
    seasons: list[int]
    parser: parsers.SquadsParser = pdt.Field(default_factory=parsers.SquadsParser)

    # io parameters
    input: datasets.LoaderKind = pdt.Field(..., discriminator="KIND")

    # client
    http_client: client.AsyncClient = pdt.Field(...)

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
                    name, id = club["tm_name"], club["tm_id"]
                    self.task_handler.create_task(
                        self._write_out(
                            session=session,
                            season=season,
                            url=self._format_url(name, id, season),
                        )
                    )
            await self.task_handler.gather_tasks()

        metrics_output = self.metrics.summary()
        logger.info("Crawler metrics: {}", metrics_output)

        return locals()  # returned for testing

    @T.override
    def _format_url(self, tm_team: str, tm_id: int, season: int) -> str:
        return self.url.format(club=tm_team, id=tm_id, season=season)
