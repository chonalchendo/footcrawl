import abc
import typing as T
from urllib.parse import parse_qs, urlparse

import pydantic as pdt
from bs4 import BeautifulSoup
from yarl import URL

from footcrawl import metrics, schemas

Items = dict[str, T.Any]


class Parser(abc.ABC, pdt.BaseModel, strict=True, frozen=True, extra="forbid"):
    @abc.abstractmethod
    def parse(self, soup: BeautifulSoup, url: URL | None = None) -> Items:
        pass

    @property
    @abc.abstractmethod
    def get_metrics(self) -> metrics.MetricsDict:
        pass


class ClubsParser(Parser):
    @T.override
    def parse(self, soup: BeautifulSoup, url: URL | None = None) -> Items:
        team_info = soup.find_all("td", {"class": "hauptlink no-border-links"})
        tm_team_name = [td.find("a").get("href").split("/")[1] for td in team_info]
        tm_team_id = [td.find("a").get("href").split("/")[4] for td in team_info]
        team_name = [td.find("a").get("title") for td in team_info]

        self.__total_items = len(tm_team_id)

        # get league and season from the url
        self.__league_name = urlparse(str(url)).path.split("/")[1]
        self.__season = parse_qs(urlparse(str(url)).query)["saison_id"][0]

        data = schemas.Clubs(
            league=self.__league_name,
            season=self.__season,
            tm_team_name=tm_team_name,
            tm_team_id=tm_team_id,
            team_name=team_name,
        )

        return data.model_dump()

    @property
    def get_metrics(self) -> metrics.MetricsDict:
        metrics_ = metrics.ParserMetrics(items_parsed=self.__total_items)
        return metrics_.summary()
