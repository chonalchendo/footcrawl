# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_clubs_parser(clubs_parser_url: str, clubs_html_sample: str):
    # Given: A mock HTML content representing a clubs table
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = clubs_html_sample
    mock_response.url = clubs_parser_url

    # When: Parsing the mock response
    parser = parsers.ClubsParser()
    results = [result async for result in parser.parse(mock_response)]

    # Then: Verify the parsed results
    assert len(results) == 1

    result = results[0]

    # Verify all schema fields are present
    expected_keys = {
        "club",
        "club_id",
        "club_link",
        "club_tm_name",
        "comp_id",
        "comp_tm_name",
        "squad_size",
        "average_age",
        "foreign_players",
        "season",
        "average_player_value",
        "total_player_value",
    }
    assert set(result.keys()) == expected_keys, (
        f"Missing keys: {expected_keys - set(result.keys())}"
    )

    # Specific assertions
    assert result["club"] == "Arsenal FC"
    assert result["squad_size"] == 40
    assert result["average_age"] == 24.6
    assert result["foreign_players"] == 23
    assert result["club_tm_name"] == "arsenal-fc"
    assert result["club_id"] == 11
    assert result["season"] == 2023
    assert result["average_player_value"] == "€30.08m"
    assert result["total_player_value"] == "€1.20bn"
    assert result["club_link"] == "/arsenal-fc/kader/verein/11/saison_id/2023"
    assert result["comp_tm_name"] == "premier-league"
    assert result["comp_id"] == "GB1"

    # Verify metrics
    metrics = parser.get_metrics
    assert metrics["items_parsed"] == 1
