import abc
import typing as T

import pydantic as pdt

from footcrawl.io import services

if T.TYPE_CHECKING:
    import aiohttp
    import bs4

    from footcrawl import metrics, schemas


type Item = dict[str, T.Any]
type SubItem = dict[str, T.Any]


class Parser(abc.ABC, pdt.BaseModel, strict=True, frozen=True, extra="forbid"):
    """A base class for parsers."""

    logger_service: services.LoggerService = pdt.Field(default=services.LoggerService())

    @abc.abstractmethod
    async def parse(self, response: "aiohttp.ClientResponse") -> Item:
        """Parse the data from the soup object returned by the client.

        Args:
            response (aiohttp.ClientResponse): The response object.

        Returns:
            Items: The parsed data.
        """
        pass

    # @abc.abstractmethod
    # def _parsers(self, row: "bs4.Tag") -> Item:
    #     pass
    #
    @property
    @abc.abstractmethod
    def get_metrics(self) -> "metrics.MetricsDict":
        """Return the metrics.

        Returns:
            metrics.MetricsDict: The metrics.
        """
        pass

    def _validate(self, data: dict[str, str], validator: "schemas.SchemaKind") -> Item:
        logger = self.logger_service.logger()
        try:
            valid_data = validator.model_validate(data)
        except pdt.ValidationError as e:
            logger.error("Validation error: {}", e)
        return valid_data.model_dump()
