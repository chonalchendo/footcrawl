# %% IMPORTS

import pytest

from footcrawl import client, crawlers, metrics, parsers
from footcrawl.io import datasets, services

# %% CRAWLER


@pytest.mark.asyncio(loop_scope="session")
async def test_competitions_crawler(
    competitions_url: str,
    logger_service: services.LoggerService,
    crawler_metrics: metrics.CrawlerMetrics,
    tmp_comp_pages: int,
    tmp_seasons: list[int],
    competitions_parser: parsers.CompetitionsParser,
    tmp_outputs_writer: datasets.AsyncNdJsonWriter,
    async_client: client.AsyncClient,
) -> None:
    # given
    # when
    crawler = crawlers.AsyncCompetitionsCrawler(
        url=competitions_url,
        logger_service=logger_service,
        metrics=crawler_metrics,
        seasons=tmp_seasons,
        pages=tmp_comp_pages,
        parser=competitions_parser,
        output=tmp_outputs_writer,
        http_client=async_client,
    )
    results = await crawler.crawl()

    # then
    assert set(results) == {
        "self",
        "logger",
        "session",
        "page",
        "metrics_output",
        "client",
    }

    # check number of items parsed,
    assert results["metrics_output"]["parser_metrics"]["items_parsed"] == 25, (
        "Did not parse the expected number items"
    )
    # check page
    assert results["page"] == 1, "Expected two keys: league name and ID"
