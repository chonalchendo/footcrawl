import pydantic as pdt
import pydantic_settings as pdts

from footcrawl import crawlers


class Settings(pdts.BaseSettings, strict=True, frozen=True, extra="forbid"):
    pass


class MainSettings(Settings):
    crawler: crawlers.CrawlerKind = pdt.Field(..., discriminator="KIND")
