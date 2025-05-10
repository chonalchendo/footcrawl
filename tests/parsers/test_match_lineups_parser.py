# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_match_lineups_parser(match_lineups_html_sample: str, match_lineups_parser_url: str):
    # Given: A mock HTML content representing a clubs table
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = match_lineups_html_sample
    mock_response.url = match_lineups_parser_url

    # When: Parsing the mock response
    parser = parsers.MatchLineupsParser()
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
        "comp_name",
        "club_id",
        "club_name",
        "club_tm_name",
        "player_id",
        "player_tm_name",
        "player_name",
        "number",
        "position",
        "current_value",
        "country",
        "misc",
        "profile_link",
        "season_stats_link",
        "is_starter"
    }
    assert set(result.keys()) == expected_keys, (
        f"Missing keys: {expected_keys - set(result.keys())}"
    )

    # Specific assertions
    assert result["match_id"] == 4361296
    assert result["matchday"] == 3
    assert result["comp_id"] == "GB1"
    assert result["comp_name"] == "Premier League"
    assert result["club_id"] == 985
    assert result['club_name'] == 'Manchester United'
    assert result["club_tm_name"] == "manchester-united"
    assert result['player_id'] == 234509
    assert result['player_tm_name'] == 'andre-onana'
    assert result['player_name'] == 'André Onana'
    assert result['number'] == 24
    assert result['position'] == 'Goalkeeper'
    assert result['current_value'] == '€35.00m'
    assert result['country'] == 'Cameroon'
    assert result['misc'] == None
    assert result['profile_link'] == "/andre-onana/profil/spieler/234509"
    assert result['season_stats_link'] == "/andre-onana/leistungsdatendetails/spieler/234509/saison/2024/wettbewerb/GB1"
    assert result['is_starter'] == True
    
    # Verify metrics
    metrics = parser.get_metrics
    assert metrics["items_parsed"] == 1
