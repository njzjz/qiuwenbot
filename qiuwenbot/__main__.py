import argparse

from qiuwenbot.entrypoints.submit import submit


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_submit = subparsers.add_parser("submit", help="Submit a task")
    parser_submit.add_argument("CONFIG", type=str, help="Path to the config file")
    parser_submit.set_defaults(func=submit)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
