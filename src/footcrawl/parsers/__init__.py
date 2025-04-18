from .base import Item
from .clubs import ClubsParser
from .fixtures import FixturesParser
from .match_lineups import MatchLineupsParser
from .squads import SquadsParser

ParserKind = ClubsParser | SquadsParser | FixturesParser | MatchLineupsParser

__all__ = [
    "ClubsParser",
    "SquadsParser",
    "FixturesParser",
    "MatchLineupsParser",
    "Item",
]
