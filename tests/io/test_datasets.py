# %% IMPORTS

import os

import pytest

from footcrawl.io import datasets

# %% WRITERS


@pytest.mark.asyncio(loop_scope="session")
async def test_async_json_writer(tmp_base_path: str, tmp_outputs_path: str) -> None:
    # given
    data = {"hello": "world", "foo": "bar"}

    writer = datasets.AsyncNdJsonWriter(base_path=tmp_base_path)
    # when
    await writer.write(data=data, output_path=tmp_outputs_path)
    # then
    assert os.path.exists(tmp_outputs_path), "Data should be written!"
