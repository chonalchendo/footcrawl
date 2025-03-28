import abc
import json
import typing as T
from pathlib import Path

import pydantic as pdt

StreamingOutput = dict[str, T.Any]
LoadedInput = list[dict[str, T.Any]]

# %% - LOADERS


class Loader(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    """Base class for all loaders.

    Args:
        path (str): Path to load the data.
    """

    KIND: str

    path: str

    @abc.abstractmethod
    def load(self, season: int) -> list[dict[str, T.Any]]:
        """Load the data from the path.

        Returns:
            list[dict[str, T.Any]]: The loaded data.
        """
        pass


class JsonLoader(Loader):
    KIND: T.Literal["JsonLoader"] = "JsonLoader"

    @T.override
    def load(self, season: int) -> list[dict[str, T.Any]]:
        if season < 2010 and season > 2024:
            raise ValueError("Season must be between 2010 and 2024.")

        formatted_path = self.__format_path(season)

        if not Path(formatted_path).exists():
            raise FileNotFoundError(f"File not found: {formatted_path}")

        with open(formatted_path, "r") as file:
            return [json.loads(line) for line in file]

    def __format_path(self, season: int) -> str:
        return self.path.format(season=season)


LoaderKind = JsonLoader

# %% - WRITERS


class Writer(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    """Base class for all writers.

    Args:
        path (str): Path to write the data.
    """

    KIND: str

    path: str

    @abc.abstractmethod
    async def write(self, data: StreamingOutput) -> None:
        """Write the data to the path.

        Args:
            data (StreamingOutput): Data to write.
        """
        pass

    def _ensure_parent_dir(self) -> None:
        """Ensure parent directory exists."""
        if not Path(self.path).parent.absolute().exists():
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)


class AsyncJsonWriter(Writer):
    """Asynchronously write data to a JSON file.

    Args:
        overwrite (bool): Overwrite the file. Defaults to True.
    """

    KIND: T.Literal["AsyncJsonWriter"] = "AsyncJsonWriter"

    overwrite: bool = pdt.Field(default=True)  # checked if true in crawler files

    @T.override
    async def write(self, data: StreamingOutput) -> None:
        self._ensure_parent_dir()

        with open(self.path, "a") as file:
            file.write(json.dumps(data) + "\n")


WriterKind = AsyncJsonWriter
