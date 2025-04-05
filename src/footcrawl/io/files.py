from pathlib import Path

import pydantic as pdt


class FileHandler(pdt.BaseModel, strict=True, frozen=False, extra="forbid"):
    """A class to handle file operations."""

    path: str = pdt.Field(default=None)

    def __init__(self, **data) -> None:
        super().__init__(**data)

        self._orig_path = self.path

    def exists(self, path: str) -> bool:
        return Path(path).exists()

    def remove(self, path: str) -> None:
        if not self.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        Path(path).unlink()

    def check_filepaths(self, seasons: int) -> None:
        for season in seasons:
            output_path_ = self._orig_path.format(season=season)
            if self.exists(path=output_path_):
                self.remove(path=output_path_)

    def format_original_path(self, season: int) -> str:
        return self._orig_path.format(season=season)

    def set_original_path(self, path: str) -> None:
        """Set the original path for the file handler."""
        self._orig_path = path

    @property
    def original_path(self) -> str:
        return self._orig_path
