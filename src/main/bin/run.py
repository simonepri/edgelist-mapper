#!/usr/bin/env python3
import argparse
import os
import sys
from typing import *  # pylint: disable=wildcard-import,unused-wildcard-import

from .compute_frequency import main as main_compute_frequency
from .generate_mapping import main as main_generate_mapping
from .map_edgelist import main as main_map_edgelist


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Map the entities and the relations of an edgelist"
    )
    parser.add_argument("edgelist", help="Path of the edgelist file")
    parser.add_argument("output", help="Path of the output directory")
    return parser.parse_args()


def normalize_args(args: argparse.Namespace) -> None:
    args.edgelist = os.path.realpath(args.edgelist)
    args.output = os.path.realpath(args.output)


def validate_args(args: argparse.Namespace) -> None:
    if not os.path.isfile(args.edgelist):
        print("The edgelist file does not exists")
        sys.exit(1)


def main(args: argparse.Namespace) -> None:
    args_compute_frequency = argparse.Namespace(
        edgelist=args.edgelist,
        ent_freq=os.path.join(args.output, "entities_frequency.tsv"),
        rel_freq=os.path.join(args.output, "relations_frequency.tsv"),
        no_header=False,
    )
    main_compute_frequency(args_compute_frequency)

    args_generate_mapping = argparse.Namespace(
        ent_freq=os.path.join(args.output, "entities_frequency.tsv"),
        rel_freq=os.path.join(args.output, "relations_frequency.tsv"),
        ent_map=os.path.join(args.output, "entities_mapping.tsv"),
        rel_map=os.path.join(args.output, "relations_mapping.tsv"),
    )
    main_generate_mapping(args_generate_mapping)

    args_map_edgelist = argparse.Namespace(
        edgelist=args.edgelist,
        ent_map=os.path.join(args.output, "entities_mapping.tsv"),
        rel_map=os.path.join(args.output, "relations_mapping.tsv"),
        mapped_edgelist=os.path.join(args.output, "mapped_edgelist.tsv"),
    )
    main_map_edgelist(args_map_edgelist)


if __name__ == "__main__":
    try:
        ARGS = parse_args()

        normalize_args(ARGS)
        validate_args(ARGS)
        main(ARGS)
    except (KeyboardInterrupt, SystemExit):
        print("\nAborted!")
