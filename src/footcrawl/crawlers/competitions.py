import typing as T

import pydantic as pdt

from footcrawl import client, parsers
from footcrawl.crawlers import base


class AsyncCompetitionsCrawler(base.Crawler):
    KIND: T.Literal["competitions"] = "competitions"

    pages: int = pdt.Field(default=25)

    seasons: list[int]
    parser: parsers.CompetitionsParser = pdt.Field(
        default_factory=parsers.CompetitionsParser
    )

    http_client: client.AsyncClient

    @T.override
    async def crawl(self) -> base.Locals:
        logger = self.logger_service.logger()

        self.file_handler.set_original_path(path=self.output.base_path)

        if self.output.overwrite:
            self.file_handler.check_filepaths(seasons=self.seasons)

        async with self.http_client as client:
            session = client.get_session

            for page in range(1, self.pages+1):
                self.task_handler.create_task(
                    self._write_out(
                        session=session,
                        season=self.seasons[0],  # current season
                        url=self._format_url(page=page),
                    )
                )
                
            await self.task_handler.gather_tasks()

            metrics_output = self.metrics.summary()
            logger.info("Crawler metrics: {}", metrics_output)

        return locals()  # returned for testing

    @T.override
    def _format_url(self, page: int) -> str:
        return self.url.format(page=page)
