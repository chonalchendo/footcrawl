import abc
import typing as T

import polars as pl
import pydantic as pdt

from footcrawl import crawlers, services
from footcrawl.io import datasets


class Source(abc.ABC, pdt.BaseModel, strict=True, frozen=True, extra="forbid"):
    KIND: str

    logger_service: services.LoggerService = services.LoggerService()

    @abc.abstractmethod
    def start(self) -> None:
        pass


class Transfermarkt(Source):
    KIND: T.Literal["Transfermarkt"] = "Transfermarkt"

    crawler: crawlers.CrawlerKind = pdt.Field(..., discriminator="KIND")
    output: datasets.WriterKind = pdt.Field(..., discriminator="KIND")

    seasons: list[int]
    leagues: list[str]

    @T.override
    def start(self) -> None:
        logger = self.logger_service.logger()
        logger.info("With logger {}", logger)
        logger.info(
            "Crawling {} for season {} in leagues {}",
            self.crawler,
            self.seasons,
            self.leagues,
        )

        for season in self.seasons:
            data = []
            for league in self.leagues:
                logger.info("Starting Crawler...")
                parsed = self.crawler.crawl(season=season, league=league)
                data.append(parsed)

            # format path
            self.output.path = self.output.path.format(season=season)

            logger.info(
                "Outputting data for season {} to path {}", season, self.output.path
            )
            data = pl.DataFrame(data)
            self.output.write(data=data)

        logger.info("Job complete.")

    @property
    def to_dataframe(self):
        return self.crawler.output_result


SourceKind = Transfermarkt
