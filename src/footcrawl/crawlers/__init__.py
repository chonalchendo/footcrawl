from .clubs import AsyncClubsCrawler
from .squads import AsyncSquadsCrawler
from .fixtures import AsyncFixturesCrawler

CrawlerKind = AsyncClubsCrawler | AsyncSquadsCrawler | AsyncFixturesCrawler

__all__ = ["AsyncClubsCrawler", "AsyncSquadsCrawler", "AsyncFixturesCrawler"]
