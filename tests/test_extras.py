import json
from pathlib import Path

import pytest

import ltoml
from . import burntsushi

DATA_DIR = Path(__file__).parent / "data" / "extras"

VALID_FILES = tuple((DATA_DIR / "valid").glob("**/*.toml"))
VALID_FILES_EXPECTED = tuple(
    json.loads(p.with_suffix(".json").read_text("utf-8")) for p in VALID_FILES
)

# INVALID_FILES = tuple((DATA_DIR / "invalid").glob("**/*.toml"))


# @pytest.mark.parametrize(
#     "invalid",
#     INVALID_FILES,
#     ids=[p.stem for p in INVALID_FILES],
# )
# def test_invalid(invalid):
#     toml_str = invalid.read_text(encoding="utf-8")
#     with pytest.raises(Exception):
#         ltoml.loads(toml_str)


@pytest.mark.parametrize(
    "valid,expected",
    zip(VALID_FILES, VALID_FILES_EXPECTED),
    ids=[p.stem for p in VALID_FILES],
)
def test_valid(valid, expected):
    toml_str = valid.read_text(encoding="utf-8")
    actual = ltoml.loads(toml_str)
    actual = burntsushi.convert(actual)
    expected = burntsushi.normalize_floats(expected)
    assert actual == expected
