import abc
import typing as T
from urllib.parse import parse_qs, urlparse

import pydantic as pdt
from bs4 import BeautifulSoup
from yarl import URL

from footcrawl import schemas


class Parser(abc.ABC, pdt.BaseModel, strict=True, frozen=True, extra="forbid"):
    @abc.abstractmethod
    def parse(self, soup: BeautifulSoup, url: URL | None = None) -> dict[str, T.Any]:
        pass


class ClubsParser(Parser):
    @T.override
    def parse(self, soup: BeautifulSoup, url: URL | None = None) -> dict[str, T.Any]:
        team_info = soup.find_all("td", {"class": "hauptlink no-border-links"})
        tm_team_name = [td.find("a").get("href").split("/")[1] for td in team_info]
        tm_team_id = [td.find("a").get("href").split("/")[4] for td in team_info]
        team_name = [td.find("a").get("title") for td in team_info]

        # get league and season from the url
        league = urlparse(str(url)).path.split("/")[1]
        season = parse_qs(urlparse(str(url)).query)["saison_id"][0]

        data = schemas.Clubs(
            league=league,
            season=season,
            tm_team_name=tm_team_name,
            tm_team_id=tm_team_id,
            team_name=team_name,
        )

        return data.model_dump()
