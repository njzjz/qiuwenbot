import json
from pathlib import Path

import pytest

from qiuwenbot.argparse import normalize

p_examples = Path(__file__).parent.parent / "examples"


@pytest.mark.parametrize(
    "p_example",
    [
        (p_examples / "filter_all.json"),
        (p_examples / "filter_new.json"),
        (p_examples / "check_duplicate.json"),
    ],
)
def test_examples(p_example):
    """Test examples."""
    with open(p_example) as f:
        config = json.load(f)
    config = normalize(config)
