from .clubs import AsyncClubsCrawler
from .fixtures import AsyncFixturesCrawler
from .match_actions import AsyncMatchActionsCrawler
from .match_lineups import AsyncMatchLineupsCrawler
from .match_stats import AsyncMatchStatsCrawler
from .squads import AsyncSquadsCrawler

CrawlerKind = (
    AsyncClubsCrawler
    | AsyncSquadsCrawler
    | AsyncFixturesCrawler
    | AsyncMatchLineupsCrawler
    | AsyncMatchActionsCrawler
    | AsyncMatchStatsCrawler
)

__all__ = [
    "AsyncClubsCrawler",
    "AsyncSquadsCrawler",
    "AsyncFixturesCrawler",
    "AsyncMatchLineupsCrawler",
    "AsyncMatchActionsCrawler",
    "AsyncMatchStatsCrawler",
]
