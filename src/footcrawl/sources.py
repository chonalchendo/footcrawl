import abc
import typing as T

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

    @T.override
    def start(self) -> None:
        logger = self.logger_service.logger()
        logger.info("With logger {}", logger)
        logger.info(
            "Crawling {} for season {} in leagues {}",
            self.crawler,
            self.crawler.seasons,
            self.crawler.leagues,
        )

        self.crawler.crawl()

    @property
    def to_dataframe(self):
        return self.crawler.output_result


SourceKind = Transfermarkt
