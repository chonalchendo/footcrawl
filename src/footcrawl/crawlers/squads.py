import typing as T

from footcrawl.crawlers import base


class SquadsCrawler(base.Crawler):
    KIND: T.Literal["Squads"] = "Squads"

    url: str

    @T.override
    async def crawl(self) -> None:
        pass
