from .base import Item
from .clubs import ClubsParser
from .squads import SquadsParser
from .fixtures import FixturesParser

ParserKind = ClubsParser | SquadsParser | FixturesParser

__all__ = ["ClubsParser", "SquadsParser", "FixturesParser", "Item"]
