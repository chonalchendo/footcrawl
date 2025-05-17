# %% IMPORTS
from unittest.mock import Mock

import pytest

from footcrawl import client, crawlers, metrics, parsers, tasks
from footcrawl.io import datasets, services

# %% CRAWLER


@pytest.mark.asyncio(loop_scope="session")
async def test_fixtures_crawler(
    fixtures_url: str,
    logger_service: services.LoggerService,
    crawler_metrics: metrics.CrawlerMetrics,
    tmp_fixtures_seasons: list[int],
    fixtures_parser: parsers.FixturesParser,
    tmp_outputs_writer: datasets.AsyncNdJsonWriter,
    mock_json_loader: Mock,
    async_client: client.AsyncClient,
    task_handler: tasks.TaskHandler
) -> None:
    # when
    crawler = crawlers.AsyncFixturesCrawler(
        url=fixtures_url,
        logger_service=logger_service,
        metrics=crawler_metrics,
        seasons=tmp_fixtures_seasons,
        parser=fixtures_parser,
        output=tmp_outputs_writer,
        input=mock_json_loader,
        http_client=async_client,
        task_handler=task_handler
    )

    results = await crawler.crawl()

    # then
    assert set(results) == {
        "self",
        "logger",
        "session",
        "season",
        "clubs",
        "club",
        "name",
        "club_id",
        "league_id",
        "metrics_output",
        "client",
    }

    # check number of items parsed,
    assert results["metrics_output"]["parser_metrics"]["items_parsed"] == 60, (
        "Did not parse the expected number items"
    )
    # check season
    assert results["season"] == 2024, "Expected season 2024"
    # check club info
    assert len(results["clubs"]) == 1, "Expected 1 club"
    assert results["name"] == "manchester-city", (
        "Expected manchester-city as the club name"
    )
    assert results["club_id"] == 281, "Expected manchester-city id 281"
