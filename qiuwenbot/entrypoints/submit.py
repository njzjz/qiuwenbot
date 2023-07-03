import argparse
import json
import os
from qiuwenbot.task.filter import FilterTask

def submit(args: argparse.Namespace):
    """Submit a task."""
    with open(args.CONFIG, "r") as f:
        config = json.load(f)
    try:
        config["password"] = os.environ["QIUWENBOT_PASSWORD"]
    except KeyError as e:
        raise KeyError("Please set environment variable QIUWENBOT_PASSWORD") from e

    task = FilterTask(**config)
    task.submit()
