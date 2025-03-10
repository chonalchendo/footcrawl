[group('check')]
check-code:
  uv run ruff check {{SOURCES}} {{TESTS}}

[group('check')]
check-format:
  uv run ruff format --check {{SOURCES}} {{TESTS}}

[group('check')]
check-type:
  uv run mypy {{SOURCES}} {{TESTS}}
