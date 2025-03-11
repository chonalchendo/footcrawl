import abc
import typing as T
from urllib.parse import parse_qs, urlparse

import httpx
import pydantic as pdt
from bs4 import BeautifulSoup

from footcrawl import constants, schemas, services, client


class Crawler(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    KIND: str

    logger_service: services.LoggerService = services.LoggerService()
    client_service: client.Client = pdt.Field(...)

    result: list[dict] | None = pdt.Field(default=None)

    @abc.abstractmethod
    def crawl(self):
        pass

    @abc.abstractmethod
    def parse(self, resp) -> dict[str, T.Any]:
        pass

    @abc.abstractmethod
    def make_request(self) -> T.Generator[httpx.Response, None, None]:
        pass

    @property
    def output_result(self) -> list[dict]:
        if self.result is None:
            raise ValueError("result is None")
        return self.result


class SquadsCrawler(Crawler):
    KIND: T.Literal["Squads"] = "Squads"
    
    url: str

    @T.override
    def crawl(self):
        pass

    @T.override
    def parse(self, resp: httpx.Response) -> dict[str, T.Any]:
        pass

    @T.override
    def make_request(self) -> T.Generator[httpx.Response, None, None]:
        pass


class ClubsCrawler(Crawler):
    KIND: T.Literal["Clubs"] = "Clubs"
    
    url: str
    seasons: list[int]
    leagues: list[str]

    @T.override
    def crawl(self):
        self.__logger = self.logger_service.logger()

        data = []
        for resp in self.make_request():
            self.__logger.info(f"Response: {resp}. Response code: {resp.status_code}")

            parsed = self.parse(resp)
            data_logger = self.__logger.bind(**parsed)
            
            data_logger.info("Data parsed")
            data.append(parsed)

        self.result = data

    @T.override
    def parse(self, resp: httpx.Response) -> dict[str, T.Any]:
        soup = BeautifulSoup(resp.text, "html.parser")
        team_info = soup.find_all("td", {"class": "hauptlink no-border-links"})
        tm_team_name = [td.find("a").get("href").split("/")[1] for td in team_info]
        tm_team_id = [td.find("a").get("href").split("/")[4] for td in team_info]
        team_name = [td.find("a").get("title") for td in team_info]

        # get league and season from the url
        url = resp.url
        league = urlparse(str(url)).path.split("/")[1]
        season = parse_qs(urlparse(str(url)).query)["saison_id"][0]

        return schemas.Clubs(
            league=league,
            season=season,
            tm_team_name=tm_team_name,
            tm_team_id=tm_team_id,
            team_name=team_name,
        ).model_dump()

    @T.override
    def make_request(self) -> T.Generator[httpx.Response, None, None]:
        for season in self.seasons:
            for league in self.leagues:
                _url = self.url.format(
                    league=league,
                    league_id=constants.LEAGUE_MAP.get(league, ""),
                    year=season,
                )
                yield self.client_service.request(url=_url)
            

CrawlerKind = ClubsCrawler | SquadsCrawler