from .clubs import AsyncClubsCrawler
from .squads import AsyncSquadsCrawler

type CrawlerKind = AsyncClubsCrawler | AsyncSquadsCrawler

__all__ = ["AsyncClubsCrawler", "AsyncSquadsCrawler"]
