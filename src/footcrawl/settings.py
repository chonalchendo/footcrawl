import pydantic as pdt
import pydantic_settings as pdts

from footcrawl import sources


class Settings(pdts.BaseSettings, strict=True, frozen=True, extra="forbid"):
    pass


class MainSettings(Settings):
    source: sources.SourceKind = pdt.Field(..., discriminator="KIND")
