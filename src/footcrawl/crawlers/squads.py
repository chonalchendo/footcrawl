import typing as T

from footcrawl.crawlers import base


class AsyncSquadsCrawler(base.Crawler):
    KIND: T.Literal["AsyncSquadsCrawler"] = "AsyncSquadsCrawler"

    @T.override
    async def crawl(self) -> base.Locals:
        return {}
