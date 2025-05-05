# %% IMPORTS

import os
import typing as T
from unittest.mock import Mock

import _pytest.logging as pl
import omegaconf
import pytest
from dotenv import load_dotenv

from footcrawl import client, metrics, parsers
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
def mock_json_loader(tmp_club_info: list[dict[str, T.Any]]) -> Mock:
    # Create a mock of the JsonLoader class
    mock_loader = Mock(spec=datasets.JsonLoader)

    # Configure the load method to return your fixture data
    mock_loader.load.return_value = tmp_club_info

    # If the crawler uses JsonLoader.KIND anywhere
    mock_loader.KIND = "JsonLoader"

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
def tmp_club_info() -> list[dict[str, T.Any]]:
    return [{"club_tm_name": "manchester-city", "club_id": 281, "comp_id": "GB1"}]


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
    caplog: pl.LogCaptureFixture, logger_service: services.LoggerService
) -> T.Generator[pl.LogCaptureFixture, None, None]:
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
