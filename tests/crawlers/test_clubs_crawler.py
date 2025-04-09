# %% IMPORTS

import pytest

from footcrawl import client, crawlers, metrics, parsers
from footcrawl.io import datasets, services

# %% CRAWLER


@pytest.mark.asyncio(loop_scope="session")
async def test_clubs_crawler(
    clubs_url: str,
    logger_service: services.LoggerService,
    crawler_metrics: metrics.CrawlerMetrics,
    tmp_seasons: list[int],
    tmp_leagues: list[dict[str, str]],
    clubs_parser: parsers.ClubsParser,
    tmp_outputs_writer: datasets.AsyncNdJsonWriter,
    async_client: client.AsyncClient,
) -> None:
    # given
    # when
    crawler = crawlers.AsyncClubsCrawler(
        url=clubs_url,
        logger_service=logger_service,
        metrics=crawler_metrics,
        seasons=tmp_seasons,
        leagues=tmp_leagues,
        parser=clubs_parser,
        output=tmp_outputs_writer,
        http_client=async_client,
    )
    results = await crawler.crawl()

    # then
    assert set(results) == {
        "self",
        "logger",
        "session",
        "league",
        "season",
        "metrics_output",
        "client",
    }

    # check number of items parsed,
    assert results["metrics_output"]["parser_metrics"]["items_parsed"] == 116, (
        "Did not parse the expected number items"
    )
    # check season
    assert results["season"] == 2024, "Expected the most recent season in season list"
    # check league
    assert len(results["league"]) == 2, "Expected two keys: league name and ID"
    assert results["league"]["name"] == "la-liga", (
        "Expected la-liga as it's the last league passed in league test fixture"
    )
    assert results["league"]["id"] == "ES1", (
        "Expected la-liga ID as it's the last league passed in league test fixture"
    )
