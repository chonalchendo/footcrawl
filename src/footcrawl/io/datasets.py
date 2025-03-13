import abc
import typing as T
from pathlib import Path

import polars as pl
import pydantic as pdt


class Writer(abc.ABC, pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    KIND: str

    @abc.abstractmethod
    def write(self, data: pl.DataFrame) -> None:
        pass


class ParquetWriter(Writer):
    KIND: T.Literal["ParquetWriter"] = "ParquetWriter"

    path: str

    @T.override
    def write(self, data: pl.DataFrame) -> None:
        if not Path(self.path).parent.absolute().exists():
            Path(self.path).parent.absolute().mkdir(parents=True, exist_ok=True)
        
        data.write_parquet(self.path)


class JsonWriter(Writer):
    KIND: T.Literal["JsonWriter"] = "JsonWriter"

    path: str

    @T.override
    def write(self, data: pl.DataFrame) -> None:
        if not Path(self.path).parent.absolute().exists():
            Path(self.path).parent.absolute().mkdir(parents=True, exist_ok=True)

        data.write_ndjson(self.path)
        

WriterKind = ParquetWriter | JsonWriter
