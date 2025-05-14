# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_competitions_parser(
    competitions_parser_url: str, competitions_html_sample: str
):
    # Given: A mock HTML content representing a clubs table
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = competitions_html_sample
    mock_response.url = competitions_parser_url

    # When: Parsing the mock response
    parser = parsers.CompetitionsParser()
    results = [result async for result in parser.parse(mock_response)]

    # Then: Verify the parsed results
    assert len(results) == 2

    result = results[0]

    # Verify all schema fields are present
    expected_keys = {
        "comp_name",
        "comp_tm_name",
        "comp_id",
        "link",
        "country",
        "tier",
        "clubs",
        "players",
        "avg_age",
        "foreigners",
        "game_ratio_of_foreigners",
        "goals_per_match",
        "avg_market_value",
        "total_market_value",
    }
    assert set(result.keys()) == expected_keys, (
        f"Missing keys: {expected_keys - set(result.keys())}"
    )

    # Specific assertions
    assert result["comp_name"] == "Premier League"
    assert result["comp_tm_name"] == "premier-league"
    assert result["comp_id"] == "GB1"
    assert result["link"] == "/premier-league/startseite/wettbewerb/GB1"
    assert result["country"] == "England"
    assert result["tier"] == "First Tier"
    assert result["clubs"] == 20
    assert result["players"] == "542"
    assert result["avg_age"] == 26.7
    assert result["foreigners"] == "67.5 %"
    assert result["game_ratio_of_foreigners"] == "71.0 %"
    assert result["goals_per_match"] == "2.94"
    assert result["avg_market_value"] == "€592.95m"
    assert result["total_market_value"] == "€11.86bn"
