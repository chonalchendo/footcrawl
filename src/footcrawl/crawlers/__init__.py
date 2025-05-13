from .clubs import AsyncClubsCrawler
from .competitions import AsyncCompetitionsCrawler
from .fixtures import AsyncFixturesCrawler
from .match_actions import AsyncMatchActionsCrawler
from .match_lineups import AsyncMatchLineupsCrawler
from .match_stats import AsyncMatchStatsCrawler
from .squads import AsyncSquadsCrawler

CrawlerKind = (
    AsyncClubsCrawler
    | AsyncCompetitionsCrawler
    | AsyncSquadsCrawler
    | AsyncFixturesCrawler
    | AsyncMatchLineupsCrawler
    | AsyncMatchActionsCrawler
    | AsyncMatchStatsCrawler
)

__all__ = [
    "AsyncClubsCrawler",
    "AsyncCompetitionsCrawler",
    "AsyncSquadsCrawler",
    "AsyncFixturesCrawler",
    "AsyncMatchLineupsCrawler",
    "AsyncMatchActionsCrawler",
    "AsyncMatchStatsCrawler",
]
