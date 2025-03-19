import argparse
import asyncio
import os
import json
import sys

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
parser.add_argument("-s", "--schema", action="store_true", help="Print settings schema and exit.")


def execute(argv: list[str] | None = None) -> int:
    args = parser.parse_args(argv)
    
    if args.schema:
        schema = settings.MainSettings.model_json_schema()
        json.dump(schema, sys.stdout, indent=4)
        return 0
    
    files = [configs.parse_file(file) for file in args.files]

    if len(files) == 0:
        raise RuntimeError("No configs provided.")

    config = configs.merge_configs(files)

    if not isinstance(config, oc.DictConfig):
        raise RuntimeError("Config is not a dictionary")

    object_ = configs.to_object(config)

    # parse user agent
    user_agent = os.getenv("USER_AGENT")
    object_["crawler"]['http_client']["headers"]["User-Agent"] = user_agent

    setting = settings.MainSettings.model_validate(object_)
    
    # start the crawler
    asyncio.run(setting.crawler.crawl())
    return 0
