from .clubs import AsyncClubsCrawler
from .fixtures import AsyncFixturesCrawler
from .squads import AsyncSquadsCrawler

CrawlerKind = AsyncClubsCrawler | AsyncSquadsCrawler | AsyncFixturesCrawler

__all__ = ["AsyncClubsCrawler", "AsyncSquadsCrawler", "AsyncFixturesCrawler"]
