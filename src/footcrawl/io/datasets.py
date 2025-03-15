import abc
import json
import typing as T
from pathlib import Path

import pydantic as pdt

StreamingOutput = dict[str, T.Any]


class Writer(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    KIND: str

    path: str

    @abc.abstractmethod
    async def write(self, data: StreamingOutput) -> None:
        pass

    def _ensure_parent_dir(self) -> None:
        if not Path(self.path).parent.absolute().exists():
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)


class AsyncJsonWriter(Writer):
    KIND: T.Literal["AsyncJsonWriter"] = "AsyncJsonWriter"

    overwrite: bool = pdt.Field(default=True)

    @T.override
    async def write(self, data: StreamingOutput) -> None:
        self._ensure_parent_dir()

        with open(self.path, "a") as file:
            file.write(json.dumps(data) + "\n")


WriterKind = AsyncJsonWriter
