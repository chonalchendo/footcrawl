import asyncio
import typing as T

import pydantic as pdt


class TaskHandler(pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)

    tasks: list[asyncio.Task] = pdt.Field(default_factory=list)

    async def gather_tasks(self) -> None:
        await asyncio.gather(*self.tasks)

    def create_task(self, coroutine: T.Coroutine) -> None:
        task = asyncio.create_task(coroutine)
        self._add_task(task)

    def _add_task(self, task: asyncio.Task) -> None:
        self.tasks.append(task)
