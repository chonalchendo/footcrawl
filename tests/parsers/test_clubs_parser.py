# %% IMPORTS

import pytest
from unittest.mock import AsyncMock
import aiohttp

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_clubs_parser():
    # Given: A mock HTML content representing a clubs table
    mock_html = """
    <html>
        <table class="items">
            <tr class="even">
                <td class="zentriert no-border-rechts"><a href="/fc-arsenal/startseite/verein/11/saison_id/2023" title="Arsenal FC"><img alt="Arsenal FC" class="tiny_wappen" src="https://tmssl.akamaized.net//images/wappen/tiny/11.png?lm=1489787850" title="Arsenal FC"/></a></td>
                <td class="hauptlink no-border-links"><a href="/fc-arsenal/startseite/verein/11/saison_id/2023" title="Arsenal FC">Arsenal FC</a> </td>
                <td class="zentriert"><a href="/arsenal-fc/kader/verein/11/saison_id/2023" title="Arsenal FC">40</a></td>
                <td class="zentriert">24.6</td>
                <td class="zentriert">23</td>
                <td class="rechts">€30.08m</td>
                <td class="rechts"><a href="/arsenal-fc/kader/verein/11/saison_id/2023" title="Arsenal FC">€1.20bn</a></td>
            </tr>
        </table>
    </html>
    """

    # Mock response object
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = mock_html

    # When: Parsing the mock response
    parser = parsers.ClubsParser()
    results = [result async for result in parser.parse(mock_response)]

    # Then: Verify the parsed results
    assert len(results) == 1

    result = results[0]

    # Verify all schema fields are present
    expected_keys = {
        "club",
        "squad_size",
        "average_age",
        "foreign_players",
        "season",
        "average_player_value",
        "total_player_value",
        "team_link",
        "tm_name",
        "tm_id",
    }
    assert (
        set(result.keys()) == expected_keys
    ), f"Missing keys: {expected_keys - set(result.keys())}"

    # Specific assertions
    assert result["club"] == "Arsenal FC"
    assert result["squad_size"] == "40"
    assert result["average_age"] == "24.6"
    assert result["foreign_players"] == "23"
    assert result["tm_name"] == "arsenal-fc"
    assert result["tm_id"] == "11"
    assert result["season"] == "2023"
    assert result["average_player_value"] == "€30.08m"
    assert result["total_player_value"] == "€1.20bn"
    assert result["team_link"] == "/arsenal-fc/kader/verein/11/saison_id/2023"

    # Verify metrics
    metrics = parser.get_metrics
    assert metrics["items_parsed"] == 1
