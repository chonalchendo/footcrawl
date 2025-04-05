from .clubs import AsyncClubsCrawler
from .squads import AsyncSquadsCrawler

CrawlerKind = AsyncClubsCrawler | AsyncSquadsCrawler

__all__ = ["AsyncClubsCrawler", "AsyncSquadsCrawler"]
