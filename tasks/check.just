# code code quality
[group('check')]
check-code:
  uv run ruff check {{SOURCES}} {{TESTS}}

# check code format
[group('check')]
check-format:
  uv run ruff format --check {{SOURCES}} {{TESTS}}

# check code typing
[group('check')]
check-type:
  uv run mypy {{SOURCES}} {{TESTS}}

# check unit tests
[group('check')]
check-test numprocesses="auto":
    uv run pytest -v -s --numprocesses={{numprocesses}} {{TESTS}}
