# %% - IMPORTS

import pytest

from footcrawl import client as client_
from footcrawl.io import services

# %% - CLIENTS


@pytest.mark.asyncio(loop_scope="session")
async def test_async_client(
    headers: dict[str, str], logger_service: services.LoggerService
) -> None:
    # given
    http_client = client_.AsyncClient(headers=headers, logger_service=logger_service)
    # when
    async with http_client as client:
        session = client.get_session
    # then
    assert session is not None, (
        "Async session should have been created with context manager!"
    )
    assert hasattr(http_client, "logger_service"), (
        "HTTP client should have an Logger service!"
    )
    assert hasattr(http_client, "headers"), "HTTP client should have headers!"


@pytest.mark.asyncio(loop_scope="session")
async def test_session_runtime_error(async_client: client_.AsyncClient) -> None:
    # given
    with pytest.raises(RuntimeError) as error:
        async_client.get_session

    # then
    assert error.match("Session not initialised. Use 'async with' context manager."), (
        "RuntimeError should be raised!"
    )
