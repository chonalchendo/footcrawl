from .clubs import AsyncClubsCrawler
from .fixtures import AsyncFixturesCrawler
from .match_actions import AsyncMatchActionsCrawler
from .match_lineups import AsyncMatchLineupsCrawler
from .squads import AsyncSquadsCrawler
from .match_stats import AsyncMatchStatsCrawler

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
    "AsyncMatchStatsCrawler"
]
