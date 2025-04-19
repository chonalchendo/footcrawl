from .clubs import AsyncClubsCrawler
from .fixtures import AsyncFixturesCrawler
from .match_lineups import AsyncMatchLineupsCrawler
from .squads import AsyncSquadsCrawler

CrawlerKind = (
    AsyncClubsCrawler
    | AsyncSquadsCrawler
    | AsyncFixturesCrawler
    | AsyncMatchLineupsCrawler
)

__all__ = [
    "AsyncClubsCrawler",
    "AsyncSquadsCrawler",
    "AsyncFixturesCrawler",
    "AsyncMatchLineupsCrawler",
]
