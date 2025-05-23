# %% IMPORTS

import os
import typing as T
from unittest.mock import Mock

import _pytest.logging as pyl
import omegaconf
import polars as pl
import pytest
from dotenv import load_dotenv

from footcrawl import client, metrics, parsers, tasks
from footcrawl.io import datasets, services

load_dotenv()

# %% FIXTURES

# %% - Paths


@pytest.fixture(scope="session")
def tests_path() -> str:
    """Return the path of the tests folder."""
    file = os.path.abspath(__file__)
    parent = os.path.dirname(file)
    return parent


@pytest.fixture(scope="function")
def tmp_base_path(tmp_path: str) -> str:
    return os.path.join(tmp_path, "base_path.json")


@pytest.fixture(scope="function")
def tmp_outputs_path(tmp_path: str) -> str:
    """Return a tmp path for the outputs dataset."""
    return os.path.join(tmp_path, "outputs.json")


@pytest.fixture(scope="session")
def confs_path(tests_path: str) -> str:
    """Return the path of the confs folder."""
    return os.path.join(tests_path, "confs")


# %% - Client


@pytest.fixture(scope="session")
def user_agent() -> str:
    """Return the user agent for the client."""
    default_user_agent = "Mozilla/5.0 Generic Browser Chrome/128.0.0.0"
    return os.getenv("USER_AGENT", default_user_agent)


@pytest.fixture(scope="session")
def headers(user_agent: str) -> dict[str, str]:
    """Return the headers for the client."""
    return {
        "User-Agent": f"{user_agent}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }


@pytest.fixture(scope="function")
def async_client(headers: dict[str, str]) -> client.AsyncClient:
    """Return an async client."""
    return client.AsyncClient(headers=headers, timeout=100)


# %% - Configs


@pytest.fixture(scope="session")
def extra_config(user_agent: str) -> str:
    """Extra config for cli script."""

    config = f"""
    {{
        "crawler": {{
            "logger_service": {{
                "level": "INFO",
            }},
            http_client: {{
                'headers': {{
                    "User-Agent": "{user_agent}"
                }}
            }}
        }}
    }}
    """
    return config


# %% - Datasets


@pytest.fixture(scope="function")
def tmp_outputs_writer(tmp_outputs_path: str) -> datasets.AsyncNdJsonWriter:
    """Return a writer for the tmp outputs dataset."""
    return datasets.AsyncNdJsonWriter(base_path=tmp_outputs_path)


@pytest.fixture(scope="function")
def mock_json_loader(tmp_club_info: pl.DataFrame) -> Mock:
    # Create a mock of the JsonLoader class
    mock_loader = Mock(spec=datasets.JsonLoader)

    # Configure the load method to return your fixture data
    mock_loader.load.return_value = tmp_club_info

    # If the crawler uses JsonLoader.KIND anywhere
    mock_loader.KIND = "json"

    return mock_loader


@pytest.fixture(scope="function")
def matchday_mock_json_loader(tmp_matchday_info: pl.DataFrame) -> Mock:
    # Create a mock of the JsonLoader class
    mock_loader = Mock(spec=datasets.JsonLoader)

    # Configure the load method to return your fixture data
    mock_loader.load.return_value = tmp_matchday_info

    # If the crawler uses JsonLoader.KIND anywhere
    mock_loader.KIND = "json"

    return mock_loader


# %% - Parsers


@pytest.fixture(scope="function")
def clubs_parser() -> parsers.ClubsParser:
    """Return a clubs parser."""
    return parsers.ClubsParser()


@pytest.fixture(scope="function")
def squads_parser() -> parsers.SquadsParser:
    """Return a clubs parser."""
    return parsers.SquadsParser()


@pytest.fixture(scope="function")
def fixtures_parser() -> parsers.FixturesParser:
    """Return a clubs parser."""
    return parsers.FixturesParser()


@pytest.fixture(scope="function")
def match_lineups_parser() -> parsers.MatchLineupsParser:
    return parsers.MatchLineupsParser()


@pytest.fixture(scope="function")
def match_stats_parser() -> parsers.MatchStatsParser:
    return parsers.MatchStatsParser()


@pytest.fixture(scope="function")
def match_actions_parser() -> parsers.MatchActionsParser:
    return parsers.MatchActionsParser()


@pytest.fixture(scope="function")
def competitions_parser() -> parsers.CompetitionsParser:
    return parsers.CompetitionsParser()


# %% - Crawlers


@pytest.fixture(scope="function")
def clubs_url() -> str:
    """Return a clubs url."""
    return "https://transfermarkt.co.uk/{league}/startseite/wettbewerb/{league_id}/plus/?saison_id={season}"


@pytest.fixture(scope="function")
def squads_url() -> str:
    """Return a squads url."""
    return (
        "https://transfermarkt.co.uk/{club}/kader/verein/{id}/saison_id/{season}/plus/1"
    )


@pytest.fixture(scope="function")
def fixtures_url() -> str:
    "Return a fixtures url."
    return "https://www.transfermarkt.co.uk/{club}/spielplan/verein/{club_id}/saison_id/{season}/plus/1#{league_id}"


@pytest.fixture(scope="function")
def match_lineups_url() -> str:
    "Return a match lineups url"
    return "https://www.transfermarkt.co.uk/{home_team}_{away_team}/aufstellung/spielbericht/{match_id}"


@pytest.fixture(scope="function")
def match_stats_url() -> str:
    return "https://www.transfermarkt.co.uk/{home_team}_{away_team}/statistik/spielbericht/{match_id}"


@pytest.fixture(scope="function")
def match_actions_url() -> str:
    return "https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/{match_id}"


@pytest.fixture(scope="function")
def competitions_url() -> str:
    return "https://www.transfermarkt.co.uk/wettbewerbe/europa/wettbewerbe?ajax=yw1&plus=2&page={page}"


@pytest.fixture(scope="function")
def tmp_comp_pages() -> int:
    return 1


@pytest.fixture(scope="function")
def tmp_seasons() -> list[int]:
    """Return a list of seasons."""
    return [2023, 2024]


@pytest.fixture(scope="function")
def tmp_squad_seasons() -> list[int]:
    """Return a list of seasons."""
    return [2024]


@pytest.fixture(scope="function")
def tmp_fixtures_seasons() -> list[int]:
    """Return a list of seasons."""
    return [2024]


@pytest.fixture(scope="function")
def tmp_matchday_seasons() -> list[int]:
    return [2024]


@pytest.fixture(scope="function")
def tmp_club_info() -> pl.DataFrame:
    club_info = [{"club_tm_name": "manchester-city", "club_id": 281, "comp_id": "GB1"}]
    return pl.DataFrame(club_info)

@pytest.fixture(scope="function")
def tmp_matchday_info() -> pl.DataFrame:
    matchday_data = [
        {
            "match_id": "4361261",
            "matchday": "1",
            "home_club_tm": "manchester-united",
            "away_club_tm": "fulham-fc",
        }
    ]
    return pl.DataFrame(matchday_data)


@pytest.fixture(scope="function")
def tmp_matchday() -> int:
    return "1"


@pytest.fixture(scope="function")
def tmp_leagues() -> list[dict[str, str]]:
    """Return a list of leagues."""
    return [
        {"name": "premier-league", "id": "GB1"},
        {"name": "bundesliga", "id": "L1"},
        {"name": "la-liga", "id": "ES1"},
    ]


# %% - Services


@pytest.fixture(scope="session", autouse=True)
def logger_service() -> T.Generator[services.LoggerService, None, None]:
    """Return and start the logger service."""
    service = services.LoggerService(colorize=False, diagnose=True)
    service.start()
    yield service
    service.stop()


@pytest.fixture
def logger_caplog(
    caplog: pyl.LogCaptureFixture, logger_service: services.LoggerService
) -> T.Generator[pyl.LogCaptureFixture, None, None]:
    """Extend pytest caplog fixture with the logger service (loguru)."""
    # https://loguru.readthedocs.io/en/stable/resources/migration.html#replacing-caplog-fixture-from-pytest-library
    logger = logger_service.logger()
    handler_id = logger.add(
        caplog.handler,
        level=0,
        format="{message}",
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)


# %% - Metrics


@pytest.fixture(scope="function")
def crawler_metrics() -> metrics.CrawlerMetrics:
    """Return a metrics object."""
    return metrics.CrawlerMetrics()


# %% - Tasks

@pytest.fixture(scope='function')
def task_handler() -> tasks.TaskHandler:
    return tasks.TaskHandler(
        max_concurrency=10,
        time_between_batches=1
    )


# %% - Resolvers


@pytest.fixture(scope="session", autouse=True)
def tests_path_resolver(tests_path: str) -> str:
    """Register the tests path resolver with OmegaConf."""

    def resolver() -> str:
        """Get tests path."""
        return tests_path

    omegaconf.OmegaConf.register_new_resolver(
        "tests_path", resolver, use_cache=True, replace=False
    )
    return tests_path


@pytest.fixture(scope="function", autouse=True)
def tmp_path_resolver(tmp_path: str) -> str:
    """Register the tmp path resolver with OmegaConf."""

    def resolver() -> str:
        """Get tmp data path."""
        return tmp_path

    omegaconf.OmegaConf.register_new_resolver(
        "tmp_path", resolver, use_cache=False, replace=True
    )
    return tmp_path
