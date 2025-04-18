import aiohttp
import pydantic as pdt

from footcrawl import metrics as metrics_
from footcrawl.io import services

# from tenacity import retry, stop_after_attempt


class AsyncClient(pdt.BaseModel, frozen=False, strict=True, extra="forbid"):
    """A client for making asynchronous HTTP requests.

    Args:
        headers (dict[str, str]): Headers to be sent with each request.
        logger_service (services.LoggerService): A logger service.
        session (aiohttp.ClientSession | None): An aiohttp session. Defaults to None.
    """

    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)

    headers: dict[str, str]
    timeout: int

    logger_service: services.LoggerService = services.LoggerService()
    session: aiohttp.ClientSession | None = pdt.Field(default=None)

    async def __aenter__(self) -> "AsyncClient":
        """Initialise the client.

        Returns:
            AsyncClient: The client instance.
        """
        logger = self.logger_service.logger()
        if self.session is None:
            logger.info("Initialising client...")
            self.session = aiohttp.ClientSession(
                timeout=self._set_timeout(self.timeout),
                headers=self.headers,
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the client."""
        if self.session and not self.session.closed:
            await self.session.close()

    @staticmethod
    def _set_timeout(timeout: int) -> aiohttp.ClientTimeout:
        return aiohttp.ClientTimeout(total=200)

    @property
    def get_session(self) -> aiohttp.ClientSession:
        """Return the session.

        Returns:
            aiohttp.ClientSession: The session.
        """
        logger = self.logger_service.logger()
        if self.session is None:
            raise RuntimeError(
                "Session not initialised. Use 'async with' context manager."
            )
        logger.info("Returning session")
        return self.session


class Response:
    def __init__(
        self, url: str, session: aiohttp.ClientSession, metrics: metrics_.CrawlerMetrics
    ) -> None:
        self.url = url
        self.session = session
        self.metrics = metrics
        self.logger_service: services.LoggerService = services.LoggerService()

    async def __call__(self, *args, **kwds):
        return await self._fetch_response()

    # @retry(stop=stop_after_attempt(3))
    async def _fetch_response(self) -> aiohttp.ClientResponse:
        logger = self.logger_service.logger()
        try:
            logger.info("Requesting URL: {}", self.url)
            resp = await self.session.get(self.url, timeout=180)
            resp.raise_for_status()
            return resp
        except aiohttp.ClientError as e:
            error = aiohttp.ClientError(f"Failed to fetch {self.url}: {e}")
            logger.error(error)
        except aiohttp.ClientResponseError as e:
            error = aiohttp.ClientResponseError(
                f"HTTP error {e.status} for {self.url}: {e.message}"
            )
            logger.error(error)
        finally:
            self.metrics.record_request(resp=resp)
