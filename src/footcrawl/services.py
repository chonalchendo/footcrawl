from __future__ import annotations

import abc
import sys
import typing as T

import loguru
import pydantic as pdt


class Service(abc.ABC, pdt.BaseModel, strict=True, frozen=True, extra="forbid"):
    @abc.abstractmethod
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass


class LoggerService(Service):
    sink: str = "stderr"
    level: str = "DEBUG"
    format: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
        "<level>{level: <8}</level>"
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
        " <level>{message}</level>"
    )
    serialize: bool = False
    colorize: bool = True
    backtrace: bool = True
    diagnose: bool = False
    catch: bool = True

    @T.override
    def start(self) -> None:
        loguru.logger.remove()
        config = self.model_dump()

        sinks = {"sys.stderr": sys.stderr, "sys.stdout": sys.stdout}
        config["sink"] = sinks.get(config["sink"], config["sink"])
        loguru.logger.add(**config)

    def logger(self) -> loguru.Logger:
        return loguru.logger
