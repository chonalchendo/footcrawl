from footcrawl.crawlers.clubs import AsyncClubsCrawler
from footcrawl.crawlers.squads import AsyncSquadsCrawler

CrawlerKind = AsyncClubsCrawler | AsyncSquadsCrawler

__all__ = ["AsyncClubsCrawler", "AsyncSquadsCrawler"]
