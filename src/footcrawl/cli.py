import argparse

from rich import print

from footcrawl import settings
from footcrawl.io import configs

parser = argparse.ArgumentParser(
    description="Run a crawler job from YAML/JSON configuration files."
)
parser.add_argument("files", nargs="*", help="Config files for the job")


def execute(argv: list[str] | None = None) -> int:
    args = parser.parse_args(argv)
    files = [configs.parse_file(file) for file in args.files]

    if len(files) == 0:
        raise RuntimeError("No configs provided.")

    config = configs.merge_configs(files)
    config.pop("globals")  # remove global values

    object_ = configs.to_object(config)
    setting = settings.MainSettings.model_validate(object_)

    print(setting)

    return 0
