from .base import Item
from .clubs import ClubsParser
from .fixtures import FixturesParser
from .squads import SquadsParser

ParserKind = ClubsParser | SquadsParser | FixturesParser

__all__ = ["ClubsParser", "SquadsParser", "FixturesParser", "Item"]
