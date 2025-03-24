# %% - IMPORTS
from collections import Counter
from unittest.mock import MagicMock

import aiohttp
import pytest

from footcrawl import metrics as metrics_

# %% - METRICS


def test_crawler_metrics() -> None:
    # given
    total_bytes = 10
    total_requests = 40
    successful_requests = 30
    failed_requests = 10
    parsed_metrics = Counter({"items_parsed": 100})

    # when
    metrics = metrics_.CrawlerMetrics(
        total_bytes_received=total_bytes,
        total_requests=total_requests,
        successful_requests=successful_requests,
        failed_requests=failed_requests,
        parser_metrics=parsed_metrics,
    )
    metrics.record_parser(metrics={"items_parsed": 10})
    results = metrics.summary()
    # then
    results.pop("scraping_time")
    assert results == {
        "total_bytes_received": 10,
        "total_requests": 40,
        "failed_requests": 10,
        "successful_requests": 30,
        "success_rate": 75.0,
        "parser_metrics": {"items_parsed": 110},
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_crawler_metrics_record_request() -> None:
    # given
    mock = aiohttp.ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.status = 200

    # when
    metrics = metrics_.CrawlerMetrics()
    async with aiohttp.ClientSession() as session:
        async with session.get("http://test.com") as response:
            metrics.record_request(resp=response)

    # then
    assert metrics.successful_requests == 1, "Successful request not recorded"
    assert metrics.total_requests == 1, "Total requests not recorded properly"


def test_crawler_metrics_record_parser_value_error(
    crawler_metrics: metrics_.CrawlerMetrics,
) -> None:
    # given
    wrong_metric = 10

    # when
    with pytest.raises(ValueError) as error:
        crawler_metrics.record_parser(metrics=wrong_metric)

    # then
    assert error.match("Metrics must be a dict class instance"), (
        "ValueError is not raised!"
    )


def test_parser_metrics() -> None:
    # given
    items_parsed = 60

    # when
    metrics = metrics_.ParserMetrics(items_parsed=items_parsed)
    results = metrics.summary()

    # then
    assert results == {"items_parsed": 60}, (
        "Items parsed has not been counted properly."
    )
