# %% IMPORTS

from unittest.mock import AsyncMock

import aiohttp
import pytest

from footcrawl import parsers

# %% PARSERS


@pytest.mark.asyncio
async def test_match_action_parser(
    match_actions_html_sample: str, match_actions_parser_url: str
):
    # Given: A mock HTML content representing a clubs table
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.text.return_value = match_actions_html_sample
    mock_response.url = match_actions_parser_url

    # When: Parsing the mock response
    parser = parsers.MatchActionsParser()
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
        "comp_tm_name",
        "season",
        "goals",
        "substitutions",
        "cards",
    }
    assert (
        set(result.keys()) == expected_keys
    ), f"Missing keys: {expected_keys - set(result.keys())}"

    # Specific assertions
    assert result["match_id"] == 4361296
    assert result["matchday"] == 3
    assert result["comp_id"] == "GB1"
    assert result["comp_tm_name"] == "premier-league"
    assert result["season"] == 2024
    assert isinstance(result["goals"], list)
    assert isinstance(result["substitutions"], list)
    assert isinstance(result["cards"], list)

    # assert number of actions is correct
    assert len(result["goals"]) == 3
    assert len(result["substitutions"]) == 8
    assert len(result["cards"]) == 5

    # validate match actions - first action in list
    goals = result["goals"][0]
    subs = result["substitutions"][0]
    cards = result["cards"][0]

    # goal actions
    assert goals["club_id"] == 31
    assert goals["club_tm_name"] == "fc-liverpool"
    assert goals["club_name"] == "Liverpool FC"
    assert goals["score"] == "0:1"
    assert goals["scorer"] == "Luis Díaz"
    assert goals["scorer_id"] == 480692
    assert goals["shot_type"] == "Header"
    assert goals["scorer_goal_season_total"] == 2
    assert goals["assister"] == " Mohamed Salah"
    assert goals["assister_id"] == 148455
    assert goals["assist_type"] == "Pass"
    assert goals["assister_assist_season_total"] == 2

    # sub actions
    assert subs["club_id"] == 985
    assert subs["club_tm_name"] == "manchester-united"
    assert subs["club_name"] == "Manchester United"
    assert subs["reason"] == ", Tactical"
    assert subs["player_off_id"] == 16306
    assert subs["player_off_tm_name"] == "casemiro"
    assert subs["player_on_id"] == 654253
    assert subs["player_on_tm_name"] == "toby-collyer"
    assert subs["player_on_name"] == "Toby Collyer"

    # card actions
    assert cards["club_id"] == 985
    assert cards["club_tm_name"] == "manchester-united"
    assert cards["club_name"] == "Manchester United"
    assert cards["player_id"] == 435648
    assert cards["player_name"] == "Joshua Zirkzee"
    assert cards["player_tm_name"] == "joshua-zirkzee"
    assert cards["card_type"] == "Yellow"
    assert cards["reason"] == "Foul"
    assert cards["player_card_type_season_total"] == 1

    # Verify metrics
    metrics = parser.get_metrics
    assert metrics["items_parsed"] == 1
