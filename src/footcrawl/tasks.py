import asyncio
import typing as T

import pydantic as pdt


class TaskHandler(pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)

    tasks: list[asyncio.Task] = pdt.Field(default_factory=list)

    max_concurrency: int = pdt.Field(default=None)
    time_between_batches: int = pdt.Field(default=None)

    def __init__(self, **data) -> None:
        super().__init__(**data)

        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(self.max_concurrency)

    async def gather_tasks(self) -> None:
        await asyncio.gather(*self.tasks)

    def create_task(self, coroutine: T.Coroutine) -> None:
        task = asyncio.create_task(
            _concurrency_limiter(coroutine, self._semaphore, self.time_between_batches)
        )
        self._add_task(task)

    def _add_task(self, task: asyncio.Task) -> None:
        self.tasks.append(task)


async def _concurrency_limiter(
    couroutine: T.Coroutine, semaphore: asyncio.Semaphore, sleep: int
) -> None:
    async with semaphore:
        await couroutine
        await asyncio.sleep(sleep)
