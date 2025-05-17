# %% IMPORTS
from unittest.mock import Mock

import pytest

from footcrawl import client, crawlers, metrics, parsers, tasks
from footcrawl.io import datasets, services

# %% CRAWLER


@pytest.mark.asyncio(loop_scope="session")
async def test_squads_crawler(
    squads_url: str,
    logger_service: services.LoggerService,
    crawler_metrics: metrics.CrawlerMetrics,
    tmp_squad_seasons: list[int],
    squads_parser: parsers.SquadsParser,
    tmp_outputs_writer: datasets.AsyncNdJsonWriter,
    mock_json_loader: Mock,
    async_client: client.AsyncClient,
    task_handler: tasks.TaskHandler
) -> None:
    # when
    crawler = crawlers.AsyncSquadsCrawler(
        url=squads_url,
        logger_service=logger_service,
        metrics=crawler_metrics,
        seasons=tmp_squad_seasons,
        parser=squads_parser,
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
        "id",
        "metrics_output",
        "client",
    }

    # check number of items parsed,
    assert results["metrics_output"]["parser_metrics"]["items_parsed"] == 28, (
        "Did not parse the expected number items"
    )
    # check season
    assert results["season"] == 2024, "Expected the most recent season in season list"
    # check club info
    assert len(results["clubs"]) == 1, "Expected two keys: league name and ID"
    assert results["name"] == "manchester-city", (
        "Expected manchester-city as the club name"
    )
    assert results["id"] == 281, "Expected manchester-city id 281"
