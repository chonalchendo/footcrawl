import aiohttp
import pydantic as pdt

from footcrawl.io import services


class AsyncClient(pdt.BaseModel, frozen=False, strict=True, extra="forbid"):
    """A client for making asynchronous HTTP requests.

    Args:
        headers (dict[str, str]): Headers to be sent with each request.
        logger_service (services.LoggerService): A logger service.
        session (aiohttp.ClientSession | None): An aiohttp session. Defaults to None.
    """

    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)

    headers: dict[str, str]

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
                headers=self.headers,
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the client."""
        if self.session and not self.session.closed:
            await self.session.close()

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
