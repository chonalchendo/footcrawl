import abc
import typing as T

import polars as pl
import pydantic as pdt


class Writer(abc.ABC, pdt.BaseModel, strict=True, frozen=True, extra="forbid"):
    KIND: str

    @abc.abstractmethod
    def write(self, data: pl.DataFrame) -> None:
        pass


class ParquetWriter(Writer):
    KIND: T.Literal["ParquetWriter"] = "ParquetWriter"

    path: str

    @T.override
    def write(self, data: pl.DataFrame) -> None:
        data.write_parquet(self.path)


class JsonWriter(Writer):
    KIND: T.Literal["JsonWriter"] = "JsonWriter"

    path: str

    @T.override
    def write(self, data: pl.DataFrame) -> None:
        data.write_json(self.path)


WriterKind = ParquetWriter | JsonWriter
