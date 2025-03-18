import aiohttp
import pydantic as pdt

from footcrawl.io import services


class AsyncClient(pdt.BaseModel, frozen=False, strict=True, extra="forbid"):
    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)

    headers: dict[str, str]
    # timeout: float = pdt.Field(default=60.0)
    rate_limit: float = pdt.Field(default=1.0)

    logger_service: services.LoggerService = services.LoggerService()
    session: aiohttp.ClientSession | None = pdt.Field(default=None)

    async def __aenter__(self) -> "AsyncClient":
        logger = self.logger_service.logger()
        if self.session is None:
            logger.info('Initialising client...')
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                # timeout=self.timeout,
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session and not self.session.closed:
            await self.session.close()

    @property
    def get_session(self) -> aiohttp.ClientSession:
        logger = self.logger_service.logger()
        if self.session is None:
            raise RuntimeError(
                "Session not initialised. Use 'async with' context manager. "
            )
        logger.info('Returning session')
        return self.session
    
