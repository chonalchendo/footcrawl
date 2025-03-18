# %% IMPORTS

import pytest

from footcrawl.io import services
from footcrawl import metrics
from footcrawl.crawlers import base

# %% CRAWLERS


@pytest.mark.asyncio(loop_scope="session")
async def test_crawler(
    logger_service: services.LoggerService, crawler_metrics: metrics.CrawlerMetrics
) -> None:
    # given
    url = "https://transfermarkt.co.uk/{league}/startseite/wettbewerb/{league_id}/plus/?saison_id={season}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

    class MyCrawler(base.Crawler):
        KIND: str = "MyCrawler"

        async def crawl(self) -> None:
            pass

    crawler = MyCrawler(url=url, headers=headers, logger_service=logger_service, crawler_metrics=crawler_metrics)

    # when
    await crawler.crawl()

    # then
    assert hasattr(crawler, "logger_service"), "Crawler should have an Logger service!"
    assert hasattr(crawler, "crawler_metrics"), "Crawler should have a metrics class!"
    assert hasattr(crawler, "url"), "Crawler should have a URL!"
    assert hasattr(crawler, "headers"), "Crawler should have headers!" 
