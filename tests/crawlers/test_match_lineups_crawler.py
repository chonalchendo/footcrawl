# %% IMPORTS
from unittest.mock import Mock

import pytest

from footcrawl import client, crawlers, metrics, parsers
from footcrawl.io import datasets, services

# %% CRAWLER


@pytest.mark.asyncio(loop_scope="session")
async def test_match_lineups_crawler(
    match_lineups_url: str,
    logger_service: services.LoggerService,
    crawler_metrics: metrics.CrawlerMetrics,
    tmp_matchday_seasons: list[int],
    tmp_matchday: int,
    match_lineups_parser: parsers.MatchLineupsParser,
    tmp_outputs_writer: datasets.AsyncNdJsonWriter,
    matchday_mock_json_loader: Mock,
    async_client: client.AsyncClient,
) -> None:
    # when
    crawler = crawlers.AsyncMatchLineupsCrawler(
        url=match_lineups_url,
        logger_service=logger_service,
        metrics=crawler_metrics,
        seasons=tmp_matchday_seasons,
        matchday=tmp_matchday,
        parser=match_lineups_parser,
        output=tmp_outputs_writer,
        input=matchday_mock_json_loader,
        http_client=async_client,
    )

    results = await crawler.crawl()

    # then
    assert set(results) == {
        "self",
        "logger",
        "session",
        "season",
        "fixtures",
        "fixture",
        "metrics_output",
        "client",
    }

    # check number of items parsed,
    assert results["metrics_output"]["parser_metrics"]["items_parsed"] == 40, (
        "Did not parse the expected number items"
    )
    # check season
    assert results["season"] == 2024, "Expected season 2024"
    # check club info
    assert len(results["fixtures"]) == 1, "Expected 1 fixture"
    
    # check fixture dataframe info
    fixture_data = results['fixtures'].to_dicts()[0]
    
    assert fixture_data['home_club_tm'] == "manchester-united", (
        "Expected home club to be manchester-united"
    )
    assert fixture_data['away_club_tm'] == 'fulham-fc', 'Expected away club to be fulham-fc'
    assert fixture_data["match_id"] == '4361261', "Expected match ID 4361261"
