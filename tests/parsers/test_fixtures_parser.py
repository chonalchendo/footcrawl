# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_fixtures_parser(fixtures_html_sample: str, fixtures_parser_url: str):
    # Given: A mock HTML content representing a clubs table
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = fixtures_html_sample
    mock_response.url = fixtures_parser_url

    # When: Parsing the mock response
    parser = parsers.FixturesParser()
    results = [result async for result in parser.parse(mock_response)]

    print(results)

    # Then: Verify the parsed results
    assert len(results) == 1

    result = results[0]

    # Verify all schema fields are present
    expected_keys = {
        "match_id",
        "matchday",
        "match_date",
        "match_time",
        "comp_id",
        "comp_tm_name",
        "comp_name",
        "season",
        "club_id",
        "club_tm_name",
        "home_club_tm",
        "home_club",
        "away_club_tm",
        "away_club",
        "formation",
        "match_report_url",
        "match_result",
        "home_team_league_position",
        "away_team_league_position",
        "attendance",
        "manager",
    }
    assert set(result.keys()) == expected_keys, (
        f"Missing keys: {expected_keys - set(result.keys())}"
    )

    # Specific assertions
    assert result["match_id"] == 4361261
    assert result["matchday"] == "1"
    assert result["match_date"] == "Fri Aug 16, 2024"
    assert result["match_time"] == "8:00 PM"
    assert result["comp_id"] == "GB1"
    assert result["comp_tm_name"] == "premier-league"
    assert result["comp_name"] == "Premier League"
    assert result["club_id"] == 985
    assert result["season"] == 2024
    assert result["club_tm_name"] == "manchester-united"
    assert result["home_club_tm"] == "manchester-united"
    assert result["home_club"] == "Manchester United"
    assert result["away_club_tm"] == "fulham-fc"
    assert result["away_club"] == "Fulham FC"
    assert result["formation"] == "4-2-3-1"
    assert result["match_report_url"] == "/spielbericht/index/spielbericht/4361261"
    assert result["match_result"] == "1:0"
    assert result["home_team_league_position"] == "15"
    assert result["away_team_league_position"] == "11"
    assert result["attendance"] == "73.297"
    assert result["manager"] == "Erik ten Hag"

    # Verify metrics
    metrics = parser.get_metrics
    assert metrics["items_parsed"] == 1
