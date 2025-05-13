# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_match_stats_parser(
    match_stats_html_sample: str, match_stats_parser_url: str
):
    # Given: A mock HTML content representing a clubs table
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = match_stats_html_sample
    mock_response.url = match_stats_parser_url

    # When: Parsing the mock response
    parser = parsers.MatchStatsParser()
    results = [result async for result in parser.parse(mock_response)]

    print(results)

    # Then: Verify the parsed results
    assert len(results) == 1

    result = results[0]

    # Verify all schema fields are present
    expected_keys = {
        "match_id",
        "matchday",
        "comp_id",
        "comp_tm_name",
        "season",
        "home_team_stats",
        "away_team_stats",
    }
    assert set(result.keys()) == expected_keys, (
        f"Missing keys: {expected_keys - set(result.keys())}"
    )

    # Specific assertions
    assert result["match_id"] == 4361296
    assert result["matchday"] == 3
    assert result["comp_id"] == "GB1"
    assert result["comp_tm_name"] == "premier-league"
    assert result["season"] == 2024
    assert isinstance(result["home_team_stats"], dict)
    assert isinstance(result["away_team_stats"], dict)

    # validate team stats
    home_stats = result["home_team_stats"]
    away_stats = result["away_team_stats"]

    # home stats
    assert home_stats["club_id"] == 985
    assert home_stats["club_tm_name"] == "manchester-united"
    assert home_stats["total_shots"] == 8
    assert home_stats["shots_off_target"] == 5
    assert home_stats["shots_saved"] == 0
    assert home_stats["corners"] == 5
    assert home_stats["free_kicks"] == 7
    assert home_stats["fouls"] == 7
    assert home_stats["offsides"] == 0

    # away stats
    assert away_stats["club_id"] == 31
    assert away_stats["club_tm_name"] == "fc-liverpool"
    assert away_stats["total_shots"] == 11
    assert away_stats["shots_off_target"] == 7
    assert away_stats["shots_saved"] == 3
    assert away_stats["corners"] == 2
    assert away_stats["free_kicks"] == 7
    assert away_stats["fouls"] == 7
    assert away_stats["offsides"] == 2

    # Verify metrics
    metrics = parser.get_metrics
    assert metrics["items_parsed"] == 1
