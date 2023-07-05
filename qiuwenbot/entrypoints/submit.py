import argparse
import json
import os

from qiuwenbot.argparse import normalize
from qiuwenbot.task.duplicate import CheckDuplicatedPageTask
from qiuwenbot.task.filter import FilterTask


def submit(args: argparse.Namespace):
    """Submit a task."""
    with open(args.CONFIG) as f:
        config = json.load(f)
    config = normalize(config)
    try:
        config["password"] = os.environ["QIUWENBOT_PASSWORD"]
    except KeyError as e:
        raise KeyError("Please set environment variable QIUWENBOT_PASSWORD") from e

    if config["task"] == "filter":
        task_class = FilterTask
    elif config["task"] == "duplicate":
        task_class = CheckDuplicatedPageTask
    else:
        raise RuntimeError("Unsupported task type")
    config.pop("task")
    task = task_class(**config)
    task.submit()
