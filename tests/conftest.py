# %% IMPORTS

import os
import typing as T

import _pytest.logging as pl
import pytest
import omegaconf
from dotenv import load_dotenv

from footcrawl import metrics
from footcrawl.io import services

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
def tmp_outputs_path(tmp_path: str) -> str:
    """Return a tmp path for the outputs dataset."""
    return os.path.join(tmp_path, "outputs.json")


@pytest.fixture(scope="session")
def confs_path(tests_path: str) -> str:
    """Return the path of the confs folder."""
    return os.path.join(tests_path, "confs")


# %% - Configs


@pytest.fixture(scope="session")
def extra_config() -> str:
    """Extra config for cli script."""

    default_user_agent = "Mozilla/5.0 Generic Browser Chrome/128.0.0.0"
    user_agent = os.getenv("USER_AGENT", default_user_agent)

    config = f"""
    {{
        "crawler": {{
            "url": "https://transfermarkt.co.uk/{{league}}/startseite/wettbewerb/{{league_id}}/plus/?saison_id={{season}}",
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


@pytest.fixture(scope="session")
def crawler_metrics() -> metrics.CrawlerMetrics:
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
