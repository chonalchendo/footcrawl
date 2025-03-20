import typing as T

import omegaconf as oc

Config = oc.ListConfig | oc.DictConfig


def parse_file(path: str) -> Config:
    return oc.OmegaConf.load(path)


def parse_string(string: str) -> Config:
    return oc.OmegaConf.create(string)


def merge_configs(configs: T.Sequence[Config]) -> Config:
    return oc.OmegaConf.merge(*configs)


def to_object(config: Config, resolve: bool = True) -> object:
    return oc.OmegaConf.to_container(config, resolve=resolve)
