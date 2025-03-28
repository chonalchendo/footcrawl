from .base import Item
from .clubs import ClubsParser
from .squads import SquadsParser

ParserKind = ClubsParser | SquadsParser

__all__ = ["ClubsParser", "SquadsParser", "Item"]
