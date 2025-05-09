# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_squads_parser(squads_html_sample: str, squads_parser_url: str):
    # Given: A mock HTML content representing a squads table
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = squads_html_sample
    mock_response.url = squads_parser_url

    # When: Parsing the mock response
    parser = parsers.SquadsParser()
    results = [result async for result in parser.parse(mock_response)]

    # Then: Verify the parsed results
    assert len(results) == 1

    result = results[0]

    # Verify all schema fields are present
    expected_keys = {
        "player_id",
        "player_tm_name",
        "player_name",
        "club_name",
        "season",
        "url",
        "position",
        "link",
        "injury_note",
        "market_value",
        "previous_value",
        "number",
        "dob",
        "age",
        "nationalities",
        "height",
        "foot",
        "signed_date",
        "transfer_fee",
        "signed_from",
        "contract_expiry",
    }
    assert set(result.keys()) == expected_keys, (
        f"Missing keys: {expected_keys - set(result.keys())}"
    )

    # Specific assertions
    assert result["player_id"] == 234509
    assert result["player_tm_name"] == "andre-onana"
    assert result["player_name"] == "André Onana"
    assert result["club_name"] == "manchester-united"
    assert result["season"] == 2024
    assert (
        result["url"]
        == "https://transfermarkt.co.uk/manchester-united/kader/verein/985/saison_id/2024/plus/1"
    )
    assert result["position"] == "Goalkeeper"
    assert result["link"] == "/andre-onana/profil/spieler/234509"
    assert result["injury_note"] == None
    assert result["market_value"] == "€32.00m"
    assert result["previous_value"] == None
    assert result["number"] == "24"
    assert result["dob"] == "Apr 2, 1996"
    assert result["age"] == 29
    assert result["nationalities"] == ["Cameroon"]
    assert result["height"] == "1,90m"
    assert result["foot"] == "right"
    assert result["signed_date"] == "Jul 20, 2023"
    assert result["transfer_fee"] == "€50.20m"
    assert result["signed_from"] == "Inter Milan"
    assert result["contract_expiry"] == "Jun 30, 2028"

    # Verify metrics
    metrics = parser.get_metrics
    assert metrics["items_parsed"] == 1
