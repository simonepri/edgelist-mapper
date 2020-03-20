#!/usr/bin/env python3
import argparse
import tempfile
import os
import sys
from typing import *  # pylint: disable=wildcard-import,unused-wildcard-import

import shelve


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Map the entities and the relations of an edgelist"
    )
    parser.add_argument("edgelist", help="Path of the edgelist file")
    parser.add_argument(
        "-em",
        "--ent-map",
        default="entities_map.tsv",
        help="Output path of the mapping for entities",
    )
    parser.add_argument(
        "-rm",
        "--rel-map",
        default="relations_map.tsv",
        help="Output path of the mapping for relations",
    )
    parser.add_argument(
        "-me",
        "--mapped-edgelist",
        default="mapped_edgelist.tsv",
        help="Output path of the mapped edgelist",
    )
    return parser.parse_args()


def normalize_args(args: argparse.Namespace) -> None:
    args.edgelist = os.path.realpath(args.edgelist)
    args.ent_map = os.path.realpath(args.ent_map)
    args.rel_map = os.path.realpath(args.rel_map)
    args.mapped_edgelist = os.path.realpath(args.mapped_edgelist)


def validate_args(args: argparse.Namespace) -> None:
    if not os.path.isfile(args.edgelist):
        print("The edgelist file does not exists")
        sys.exit(1)
    if not os.path.isfile(args.ent_map):
        print("The entities mapping file does not exists")
        sys.exit(1)
    if not os.path.isfile(args.rel_map):
        print("The relations mapping file does not exists")
        sys.exit(1)


def main(args: argparse.Namespace) -> None:
    edgelist_path = args.edgelist
    ent_map_path = args.ent_map
    rel_map_path = args.rel_map
    el_map_path = args.mapped_edgelist

    with tempfile.TemporaryDirectory() as tmp:
        ent_dict_path = os.path.join(tmp, "ent")
        rel_dict_path = os.path.join(tmp, "rel")

        with shelve.open(ent_dict_path) as rel_dict, shelve.open(
            rel_dict_path
        ) as ent_dict:
            print("Processing entities mapping")
            with open(ent_map_path, "r") as em_handle:
                for line in em_handle:
                    parts = line.rstrip("\n").split("\t")
                    ent_dict[parts[1]] = parts[0]

            print("Processing relations mapping")
            with open(rel_map_path, "r") as rm_handle:
                for line in rm_handle:
                    parts = line.rstrip("\n").split("\t")
                    rel_dict[parts[1]] = parts[0]

            print("Writing the mapped edgelist")
            os.makedirs(os.path.dirname(el_map_path), exist_ok=True)
            with open(el_map_path, "w+") as mel_handle, open(
                edgelist_path, "r"
            ) as el_handle:
                for line in el_handle:
                    parts = line.rstrip("\n").split("\t")
                    mel_handle.write(
                        ent_dict[parts[0]]
                        + "\t"
                        + rel_dict[parts[1]]
                        + "\t"
                        + ent_dict[parts[2]]
                        + "\n"
                    )


if __name__ == "__main__":
    try:
        ARGS = parse_args()

        normalize_args(ARGS)
        validate_args(ARGS)
        main(ARGS)
    except (KeyboardInterrupt, SystemExit):
        print("\nAborted!")
