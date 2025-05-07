# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_squads_parser():
    # Given: A mock HTML content representing a squads table
    mock_html = """
    <html>
        <table class="items">
        <thead>
        <tr>
        <th class="zentriert" id="yw1_c0"><a class="sort-link asc" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/trikotNumber.desc">#</a></th><th id="yw1_c1"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/name">Player</a></th><th class="zentriert" id="yw1_c2"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/dateOfBirthTimestamp">Date of birth/Age</a></th><th class="zentriert" id="yw1_c3">Nat.</th><th class="zentriert" id="yw1_c4"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/size.desc">Height</a></th><th class="zentriert" id="yw1_c5"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/foot.desc">Foot</a></th><th class="zentriert" id="yw1_c6"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/teamMemberSinceTimestamp">Joined</a></th><th class="zentriert" id="yw1_c7">Signed from</th><th class="zentriert" id="yw1_c8"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/contractEndTimestamp">Contract</a></th><th class="rechts" id="yw1_c9"><a class="sort-link desc" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/marketValueRaw">Market value</a></th></tr>
        </thead>
        <tbody>
        <tr class="odd">
        <td class="zentriert rueckennummer bg_Torwart" title="Goalkeeper"><div class="rn_nummer">24</div></td><td class="posrela">
        <table class="inline-table">
        <tr>
        <td rowspan="2">
        <img alt="André Onana" class="bilderrahmen-fixed lazy lazy" data-src="https://img.a.transfermarkt.technology/portrait/medium/234509-1686929812.jpg?lm=1" src="data:image/gif;base64,R0lGODlhAQABAIAAAMLCwgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" title="André Onana"> </img></td>
        <td class="hauptlink">
        <a href="/andre-onana/profil/spieler/234509">
                        André Onana            </a>
        </td>
        </tr>
        <tr>
        <td>
                    Goalkeeper        </td>
        </tr>
        </table>
        </td><td class="zentriert">Apr 2, 1996 (29)</td><td class="zentriert"><img alt="Cameroon" class="flaggenrahmen" src="https://tmssl.akamaized.net//images/flagge/verysmall/31.png?lm=1520611569" title="Cameroon"/></td><td class="zentriert">1,90m</td><td class="zentriert">right</td><td class="zentriert">Jul 20, 2023</td><td class="zentriert"><a href="/inter-mailand/startseite/verein/46/saison_id/2023" title="Inter Milan: Ablöse €50.20m"><img alt="Inter Milan" class="" src="https://tmssl.akamaized.net//images/wappen/verysmall/46.png?lm=1618900989" title="Inter Milan"/></a></td><td class="zentriert">Jun 30, 2028</td><td class="rechts hauptlink"><a href="/andre-onana/marktwertverlauf/spieler/234509">€32.00m</a></td></tr>
    </html>
    """
    mock_url = "https://transfermarkt.co.uk/manchester-united/kader/verein/985/saison_id/2024/plus/1"

    # Mock response object
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = mock_html
    mock_response.url = mock_url

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
