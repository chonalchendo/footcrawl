# %% IMPORTS

from bs4 import BeautifulSoup
from yarl import URL

from footcrawl import parsers

# %% PARSERS


def test_clubs_parser() -> None:
    # given
    mock_html = """
    <table>
        <tr>
            <td class="hauptlink no-border-links">
                <a href="/fc-bayern/startseite/verein/12345/saison_id/2023" title="FC Bayern Munich">FC Bayern Munich Link</a>
            </td>
            <td class="hauptlink no-border-links">
                <a href="/borussia-dortmund/startseite/verein/67890/saison_id/2023" title="Borussia Dortmund">Borussia Dortmund Link</a>
            </td>
        </tr>
    </table>
    """

    soup = BeautifulSoup(mock_html, "html.parser")
    mock_url = URL("https://example.com/bundesliga?saison_id=2023")

    # when
    clubs_parser = parsers.ClubsParser()
    result = clubs_parser.parse(soup, mock_url)

    # then
    assert result["league"] == "bundesliga"
    assert result["season"] == 2023
    assert result["team_name"] == ["FC Bayern Munich", "Borussia Dortmund"]
    assert result["tm_team_name"] == ["fc-bayern", "borussia-dortmund"]
    assert result["tm_team_id"] == [12345, 67890]

    # verify metrics
    metrics = clubs_parser.get_metrics
    assert metrics["items_parsed"] == 2


def test_clubs_parser_empty_input() -> None:
    # given
    empty_soup = BeautifulSoup("<html></html>", "html.parser")
    mock_url = URL("https://example.com/bundesliga?saison_id=2023")

    # when
    clubs_parser = parsers.ClubsParser()
    result = clubs_parser.parse(empty_soup, mock_url)

    # then
    assert result["league"] == "bundesliga"
    assert result["season"] == 2023
    assert result["team_name"] == []
    assert result["tm_team_name"] == []
    assert result["tm_team_id"] == []

    # Verify metrics
    metrics = clubs_parser.get_metrics
    assert metrics["items_parsed"] == 0
