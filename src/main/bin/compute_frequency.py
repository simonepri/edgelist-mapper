#!/usr/bin/env python3
import argparse
import tempfile
import os
import sys
from typing import *  # pylint: disable=wildcard-import,unused-wildcard-import

import shelve

from .. import utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute the frequency of each entity and relation"
        + " of a multi-relational graph"
    )
    parser.add_argument("edgelist", help="Path of the edgelist file")
    parser.add_argument(
        "-ef",
        "--ent-freq",
        default="entities_frequency.tsv",
        help="Output path of the frequency file for entities",
    )
    parser.add_argument(
        "-rf",
        "--rel-freq",
        default="relations_frequency.tsv",
        help="Output path of the frequency file for relations",
    )
    parser.add_argument(
        "-nh",
        "--no-header",
        type=bool,
        default=False,
        help="If you pass this the first line of the edgelist will be ignored",
    )
    return parser.parse_args()


def normalize_args(args: argparse.Namespace) -> None:
    args.edgelist = os.path.realpath(args.edgelist)
    args.ent_freq = os.path.realpath(args.ent_freq)
    args.rel_freq = os.path.realpath(args.rel_freq)


def validate_args(args: argparse.Namespace) -> None:
    if not os.path.isfile(args.edgelist):
        print("The edgelist file does not exists")
        sys.exit(1)


def main(args: argparse.Namespace) -> None:
    edgelist_path = args.edgelist
    ent_freq_path = args.ent_freq
    rel_freq_path = args.rel_freq

    with tempfile.TemporaryDirectory() as tmp:
        ent_dict_path = os.path.join(tmp, "ent")
        rel_dict_path = os.path.join(tmp, "rel")

        with shelve.open(ent_dict_path) as ent_dict, shelve.open(
            rel_dict_path
        ) as rel_dict:

            print("Computing the frequencies for entities and relations")
            with open(edgelist_path, "r") as el_handle:
                utils.frequencies_from_edgelist(
                    edgelist=el_handle,
                    delimiter="\t",
                    lhs_store=ent_dict,
                    rhs_store=ent_dict,
                    rel_store=rel_dict,
                    lhs_col=0,
                    rhs_col=2,
                    rel_col=1,
                    has_header=args.no_header,
                )

            print("Writing the frequency file for entities")
            os.makedirs(os.path.dirname(ent_freq_path), exist_ok=True)
            with open(ent_freq_path, "w+") as ef_handle:
                for ent in ent_dict:
                    ef_handle.write("%s\t%d\n" % (ent, ent_dict[ent]))

            print("Writing the frequency file for relations")
            os.makedirs(os.path.dirname(rel_freq_path), exist_ok=True)
            with open(rel_freq_path, "w+") as rf_handle:
                for rel in rel_dict:
                    rf_handle.write("%s\t%d\n" % (rel, rel_dict[rel]))

            print("Sorting the frequency file for entities")
            utils.sort_file(
                ent_freq_path,
                delimiter="\t",
                column=1,
                has_header=False,
                reverse=True,
                numerical=True,
            )

            print("Sorting the frequency file for relations")
            utils.sort_file(
                rel_freq_path,
                delimiter="\t",
                column=1,
                has_header=False,
                reverse=True,
                numerical=True,
            )


if __name__ == "__main__":
    try:
        ARGS = parse_args()

        normalize_args(ARGS)
        validate_args(ARGS)
        main(ARGS)
    except (KeyboardInterrupt, SystemExit):
        print("\nAborted!")
