# %% IMPORTS

import pytest

from footcrawl import metrics
from footcrawl.crawlers import base
from footcrawl.io import services

# %% CRAWLERS


@pytest.mark.asyncio(loop_scope="session")
async def test_crawler(
    logger_service: services.LoggerService, crawler_metrics: metrics.CrawlerMetrics
) -> None:
    # given
    url = "https://transfermarkt.co.uk/{league}/startseite/wettbewerb/{league_id}/plus/?saison_id={season}"

    class MyCrawler(base.Crawler):
        KIND: str = "MyCrawler"

        async def crawl(self) -> None:
            pass

    crawler = MyCrawler(
        url=url,
        logger_service=logger_service,
        crawler_metrics=crawler_metrics,
    )

    # when
    await crawler.crawl()

    # then
    assert hasattr(crawler, "logger_service"), "Crawler should have an Logger service!"
    assert hasattr(crawler, "crawler_metrics"), "Crawler should have a metrics class!"
    assert hasattr(crawler, "url"), "Crawler should have a URL!"
    assert hasattr(crawler, "headers"), "Crawler should have headers!"
