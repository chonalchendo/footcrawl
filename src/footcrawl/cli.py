import argparse
import json
import os
import sys
import uvloop

import omegaconf as oc
from dotenv import load_dotenv

from footcrawl import settings
from footcrawl.io import configs

# load env variables
load_dotenv()


parser = argparse.ArgumentParser(
    description="Run a crawler job from YAML/JSON configuration files."
)
parser.add_argument("files", nargs="*", help="Config files for the job")
parser.add_argument(
    "--seasons", nargs="*", type=int, help="Pass seasons to crawl from CLI"
)
parser.add_argument(
    "-s", "--schema", action="store_true", help="Print settings schema and exit."
)
parser.add_argument(
    "-e", "--extras", nargs="*", default=[], help="Config strings for the job."
)


def execute(argv: list[str] | None = None) -> int:
    """Execute the CLI with the given arguments."""
    args = parser.parse_args(argv)

    if args.schema:
        schema = settings.MainSettings.model_json_schema()
        json.dump(schema, sys.stdout, indent=4)
        return 0

    files = [configs.parse_file(file) for file in args.files]
    strings = [configs.parse_string(string) for string in args.extras]

    if len(files) == 0:
        raise RuntimeError("No configs provided.")

    config = configs.merge_configs([*files, *strings])

    if not isinstance(config, oc.DictConfig):
        raise RuntimeError("Config is not a dictionary")

    object_ = configs.to_object(config)

    # parse user agent
    user_agent = os.getenv("USER_AGENT")
    object_["crawler"]["http_client"]["headers"]["User-Agent"] = user_agent

    # update seasons with cli args
    if args.seasons:
        object_["crawler"]["seasons"] = args.seasons

    setting = settings.MainSettings.model_validate(object_)

    # start the crawler
    uvloop.run(setting.crawler.crawl())
    return 0
