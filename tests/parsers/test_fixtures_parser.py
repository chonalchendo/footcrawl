# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_fixtures_parser():
    # Given: A mock HTML content representing a clubs table
    mock_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Premier League Information</title>
    <meta charset="UTF-8">
</head>
<body>
    <div class="box"></div>
    <div class="box"></div>
    <div class="box"></div>
    <div class="box">
        <h2 class="content-box-headline content-box-headline--inverted content-box-headline--logo 
        content-box-headline--bottom-bordered content-box-headline--extra-space">
            <a href="/premier-league/startseite/wettbewerb/GB1/saison_id/2024" name="GB1">
                <img alt="Premier League" class="" src="https://tmssl.akamaized.net//images/logo/medium/gb1.png?lm=1521104656" 
                title="Premier League"/>Premier League
            </a>
        </h2>
        <div class="tm-tabs">
            <a class="tm-tab" href="/manchester-united/spielplan/verein/985/saison_id/2024#GB1">
                <div class=""><span>Compact</span></div>
            </a>
            <a class="tm-tab tm-tab__active--parent" href="/manchester-united/spielplan/verein/985/saison_id/2024/plus/1#GB1">
                <div class="tm-tab__active"><span>Detailed</span></div>
            </a>
        </div>
        <div class="responsive-table">
            <table>
                <thead>
                    <tr>
                        <th class="zentriert">Matchday</th>
                        <th class="zentriert">Date</th>
                        <th class="zentriert">Time</th>
                        <th colspan="2">Home team</th>
                        <th colspan="2">Away team</th>
                        <th class="zentriert">System of play</th>
                        <th>Coach</th>
                        <th class="rechts">Attendance</th>
                        <th class="zentriert">Result</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td class="zentriert">
                    <a href="/test/spieltag/wettbewerb/GB1/saison_id/2024/spieltag/1">1</a> </td>
                    <td class="zentriert">
                                                            Fri Aug 16, 2024                                    </td>
                    <td class="zentriert">
                                                            8:00 PM                                    </td>
                    <td class="zentriert no-border-rechts">
                    <a href="/manchester-united/startseite/verein/985"><img alt="Manchester United" class="lazy" 
                    data-src="https://tmssl.akamaized.net//images/wappen/profil/985.png?lm=1457975903" 
                    src="data:image/gif;base64,R0lGODlhAQABAIAAAMLCwgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" style="max-width: 15px;" 
                    title="Manchester United"/></a> </td>
                    <td class="no-border-links hauptlink">
                    <a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United">Man Utd</a> <span 
                    class="tabellenplatz">(15.)</span> </td>
                    <td class="zentriert no-border-rechts">
                    <a href="/fulham-fc/startseite/verein/931"><img alt="Fulham FC" class="lazy" 
                    data-src="https://tmssl.akamaized.net//images/wappen/profil/931.png?lm=1556831687" 
                    src="data:image/gif;base64,R0lGODlhAQABAIAAAMLCwgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" style="max-width: 15px;" 
                    title="Fulham FC"/></a> </td>
                    <td class="no-border-links 1">
                    <a href="/fc-fulham/startseite/verein/931/saison_id/2024" title="Fulham FC">Fulham</a> <span 
                    class="tabellenplatz">(11.)</span> </td>
                    <td class="zentriert">
                                                                4-2-3-1                                        </td>
                    <td><a href="/erik-ten-hag/profil/trainer/3816" id="0" title="Erik ten Hag">Erik ten Hag</a></td>
                    <td class="rechts">
                                                                73.297                                        </td>
                    <td class="zentriert"><a class="ergebnis-link" href="/spielbericht/index/spielbericht/4361261" id="4361261" 
                    title="Match report"><span class="greentext">1:0 </span></a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
    """
    mock_url = "https://www.transfermarkt.co.uk/manchester-united/spielplan/verein/985/saison_id/2024/plus/1#GB1"

    # Mock response object
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = mock_html
    mock_response.url = mock_url

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
