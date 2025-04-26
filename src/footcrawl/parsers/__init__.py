from .base import Item
from .clubs import ClubsParser
from .fixtures import FixturesParser
from .match_actions import MatchActionsParser
from .match_lineups import MatchLineupsParser
from .squads import SquadsParser
from .match_stats import MatchStatsParser

ParserKind = (
    ClubsParser
    | SquadsParser
    | FixturesParser
    | MatchLineupsParser
    | MatchActionsParser
    | MatchStatsParser
)

__all__ = [
    "ClubsParser",
    "SquadsParser",
    "FixturesParser",
    "MatchLineupsParser",
    "MatchActionsParser",
    "MatchStatsParser",
    "Item",
]
