import argparse
import asyncio

import omegaconf as oc

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

    if not isinstance(config, oc.DictConfig):
        raise RuntimeError("Config is not a dictionary")

    object_ = configs.to_object(config)
    setting = settings.MainSettings.model_validate(object_)

    # start the crawler
    asyncio.run(setting.crawler.crawl())
    return 0
