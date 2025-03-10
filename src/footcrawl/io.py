import abc
import typing as T

import polars as pl
import pydantic as pdt


class Writer(abc.ABC, pdt.BaseModel, strict=True, frozen=True, extra="forbid"):
    path: str

    @abc.abstractmethod
    def write(self, data: pl.DataFrame) -> None:
        pass


class ParquetWriter(Writer):
    @T.override
    def write(self, data: pl.DataFrame) -> None:
        data.write_parquet(self.path)
