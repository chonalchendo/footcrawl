# %% IMPORTS

import os

import pytest

from footcrawl.io import datasets

# %% WRITERS


@pytest.mark.asyncio(loop_scope="session")
async def test_async_json_writer(tmp_outputs_path: str) -> None:
    # given
    data = {"hello": "world", "foo": "bar"}

    writer = datasets.AsyncJsonWriter(path=tmp_outputs_path)
    # when
    await writer.write(data=data)
    # then
    assert os.path.exists(tmp_outputs_path), "Data should be written!"
