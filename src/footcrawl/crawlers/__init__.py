from footcrawl.crawlers.clubs import AsyncClubsCrawler
from footcrawl.crawlers.squads import SquadsCrawler

CrawlerKind = SquadsCrawler | AsyncClubsCrawler

__all__ = ["ClubsCrawler", "SquadsCrawler"]
