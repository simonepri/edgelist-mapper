#!/usr/bin/env python3
import argparse
import os
import sys
from typing import *  # pylint: disable=wildcard-import,unused-wildcard-import


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Builds a mapping from each named entity and relation"
        + " of a multi-relational graph to an int"
    )
    parser.add_argument(
        "-ef",
        "--ent-freq",
        default="entities_frequency.tsv",
        help="Path of the frequency file for entities",
    )
    parser.add_argument(
        "-rf",
        "--rel-freq",
        default="relations_frequency.tsv",
        help="Path of the frequency file for relations",
    )
    parser.add_argument(
        "-rm",
        "--rel-map",
        default="relations_map.tsv",
        help="Output path of the mapping for entities",
    )
    parser.add_argument(
        "-em",
        "--ent-map",
        default="entities_map.tsv",
        help="Output path of the mapping for relations",
    )
    return parser.parse_args()


def normalize_args(args: argparse.Namespace) -> None:
    args.ent_freq = os.path.realpath(args.ent_freq)
    args.rel_freq = os.path.realpath(args.rel_freq)
    args.ent_map = os.path.realpath(args.ent_map)
    args.rel_map = os.path.realpath(args.rel_map)


def validate_args(args: argparse.Namespace) -> None:
    if not os.path.isfile(args.ent_freq):
        print("The entities frequency file does not exists")
        sys.exit(1)
    if not os.path.isfile(args.rel_freq):
        print("The relations frequency file does not exists")
        sys.exit(1)


def main(args: argparse.Namespace) -> None:
    ent_freq_path = args.ent_freq
    rel_freq_path = args.rel_freq
    ent_map_path = args.ent_map
    rel_map_path = args.rel_map

    print("Writing the mapping file for entities")
    os.makedirs(os.path.dirname(ent_map_path), exist_ok=True)
    with open(ent_map_path, "w+") as em_handle:
        with open(ent_freq_path, "r") as ef_handle:
            for idx, line in enumerate(ef_handle):
                parts = line.rstrip("\n").split("\t", 1)
                em_handle.write(str(idx) + "\t" + parts[0] + "\n")

    print("Writing the mapping file for relations")
    os.makedirs(os.path.dirname(rel_map_path), exist_ok=True)
    with open(rel_map_path, "w+") as rm_handle:
        with open(rel_freq_path, "r") as rf_handle:
            for idx, line in enumerate(rf_handle):
                parts = line.rstrip("\n").split("\t", 1)
                rm_handle.write(str(idx) + "\t" + parts[0] + "\n")


if __name__ == "__main__":
    try:
        ARGS = parse_args()

        normalize_args(ARGS)
        validate_args(ARGS)
        main(ARGS)
    except (KeyboardInterrupt, SystemExit):
        print("\nAborted!")
