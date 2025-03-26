import pydantic as pdt
import pydantic_settings as pdts

from footcrawl import crawlers


class Settings(pdts.BaseSettings, strict=True, frozen=True, extra="forbid"):
    """Base class for settings."""

    pass


class MainSettings(Settings):
    """Main settings for the project.

    Args:
        crawler (crawlers.CrawlerKind): The crawler to run.
    """

    crawler: crawlers.CrawlerKind = pdt.Field(..., discriminator="KIND")
