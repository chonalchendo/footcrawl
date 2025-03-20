# %% IMPORTS
import json
import os
import pytest
import pydantic as pdt
from _pytest import capture as pc
from footcrawl import cli

# %% CLI SCRIPTS


def test_schema(capsys: pc.CaptureFixture[str]) -> None:
    """Test that project schema loads properly.

    Args:
        capsys (pc.CaptureFixture[str]): capture system fixture
    """
    # given
    args = ["prog", "--schema"]
    # when
    cli.execute(args)
    captured = capsys.readouterr()
    # then
    assert captured.err == "", "Captured error should be empty!"
    assert json.loads(captured.out), "Captured output should be a JSON!"


@pytest.mark.parametrize(
    "scenario",
    [
        "valid",
        pytest.param(
            "invalid",
            marks=pytest.mark.xfail(
                reason="Invalid config.",
                raises=pdt.ValidationError,
            ),
        ),
    ],
)
def test_execute(scenario: str, confs_path: str, extra_config: str) -> None:
    """Test the execute function that runs the project. Mulitple config files
    are passed to the command line and we expect them to run properly with 0
    returned.

    Args:
        scenario (str): valid or invalid scenario
        confs_path (str): path to test configs
        extra_config (str): extra config fixture
    """
    # given
    folder = os.path.join(confs_path, scenario)
    confs = list(sorted(os.listdir(folder)))
    # when
    for conf in confs:  # one job per config
        config = os.path.join(folder, conf)
        argv = [config, "-e", extra_config]
        status = cli.execute(argv=argv)
        # then
        assert status == 0, f"Job should succeed for config: {config}"
        

def test_execute__no_configs() -> None:
    """Test that execute function returns RunTimeError when no configs
    are passed to it.
    """
    # given
    argv: list[str] = []
    # when
    with pytest.raises(RuntimeError) as error:
        cli.execute(argv)
    # then
    assert error.match("No configs provided."), "RuntimeError should be raised!"
