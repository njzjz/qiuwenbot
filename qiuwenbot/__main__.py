import argparse

from qiuwenbot.entrypoints.gui import start_dpgui
from qiuwenbot.entrypoints.submit import submit


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # submit
    parser_submit = subparsers.add_parser("submit", help="Submit a task")
    parser_submit.add_argument("CONFIG", type=str, help="Path to the config file")
    parser_submit.set_defaults(func=submit)

    # gui
    parser_gui = subparsers.add_parser(
        "gui",
        help="Serve DP-GUI.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_gui.add_argument(
        "-p",
        "--port",
        type=int,
        default=6042,
        help="The port to serve DP-GUI on.",
    )
    parser_gui.add_argument(
        "--bind_all",
        action="store_true",
        help=(
            "Serve on all public interfaces. This will expose your DP-GUI instance "
            "to the network on both IPv4 and IPv6 (where available)."
        ),
    )
    parser_gui.set_defaults(func=start_dpgui)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
