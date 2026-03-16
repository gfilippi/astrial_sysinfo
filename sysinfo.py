#!/usr/bin/env python3

import json
import argparse
from pathlib import Path

from core.loader import discover_plugins


PLUGIN_DIR = Path(__file__).parent / "plugins"


def gather():

    plugins = discover_plugins(PLUGIN_DIR)

    result = {
        "hardware": {},
        "software": {},
        "metadata": {}
    }

    context = {}

    for plugin in plugins:

        try:

            data = plugin.gather(context)

            result[plugin.section].update(data)

        except Exception as e:

            result["metadata"].setdefault(
                "plugin_errors", {}
            )[plugin.name] = str(e)

    return result


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json"
    )

    args = parser.parse_args()

    data = gather()

    if args.format == "json":

        print(json.dumps(data, indent=2))

    else:

        import yaml

        print(yaml.dump(data, sort_keys=False))


if __name__ == "__main__":
    main()
