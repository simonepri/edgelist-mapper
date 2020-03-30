#!/usr/bin/env python3
from typing import *  # pylint: disable=wildcard-import,unused-wildcard-import
from typing import IO

import os
import shlex


def sort_file(
    input_filename: str,
    column: int,
    output_filename: Optional[str] = None,
    has_header: bool = False,
    delimiter: str = "\t",
    reverse: bool = False,
    numerical: bool = False,
) -> None:
    flags = ""
    if output_filename is None:
        output_filename = input_filename
    if reverse:
        flags += "-r "
    if numerical:
        flags += "-n "
    sortcmd = "sort %s-k %d -t %s -o %s %s" % (
        flags,
        column + 1,
        shlex.quote(delimiter),
        output_filename,
        input_filename,
    )
    if has_header:
        raise ValueError("Not Implemented")
    os.system(sortcmd)


def readlines_reverse(filename: str) -> Generator[str, None, None]:
    with open(filename, "rt") as qfile:
        qfile.seek(0, os.SEEK_END)
        position = qfile.tell()
        line = ""
        while position >= 0:
            qfile.seek(position)
            next_char = qfile.read(1)
            if next_char == "\n":
                yield line[::-1]
                line = ""
            else:
                line += next_char
            position -= 1
        yield line[::-1]


def frequencies_from_edgelist(
    edgelist: IO,
    lhs_store: Optional[MutableMapping[str, int]] = None,
    rhs_store: Optional[MutableMapping[str, int]] = None,
    rel_store: Optional[MutableMapping[str, int]] = None,
    lhs_col: Optional[int] = None,
    rhs_col: Optional[int] = None,
    rel_col: Optional[int] = None,
    delimiter: Optional[str] = "\t",
    has_header: bool = False,
) -> None:
    if lhs_col is None and rhs_col is None and rel_col is None:
        raise ValueError(
            "At least one of lhs_col, rhs_col, rel_col must be specified"
        )

    if lhs_col is not None and lhs_store is None:
        raise ValueError(
            "If lhs_col is specified, lhs_store must be provided as well"
        )
    if rhs_col is not None and rhs_store is None:
        raise ValueError(
            "If rhs_col is specified, rhs_store must be provided as well"
        )
    if rel_col is not None and rel_store is None:
        raise ValueError(
            "If rel_col is specified, rel_store must be provided as well"
        )

    for edge in edgelist:
        if has_header is True:
            has_header = False
            continue
        parts = edge.rstrip("\n").split(delimiter)

        if lhs_col is not None and lhs_store is not None:
            if lhs_col < 0 or lhs_col >= len(parts):
                raise ValueError(
                    "lhs_col must be in range (%d, %d) but %d provided"
                    % (0, len(parts), lhs_col)
                )
            lhs_key = parts[lhs_col]
            lhs_store[lhs_key] = (
                lhs_store[lhs_key] + 1 if lhs_key in lhs_store else 1
            )

        if rhs_col is not None and rhs_store is not None:
            if rhs_col < 0 or rhs_col >= len(parts):
                raise ValueError(
                    "rhs_col must be in range (%d, %d) but %d provided"
                    % (0, len(parts), rhs_col)
                )
            rhs_key = parts[rhs_col]
            rhs_store[rhs_key] = (
                rhs_store[rhs_key] + 1 if rhs_key in rhs_store else 1
            )

        if rel_col is not None and rel_store is not None:
            if rel_col < 0 or rel_col >= len(parts):
                raise ValueError(
                    "rel_col must be in range (%d, %d) but %d provided"
                    % (0, len(parts), rel_col)
                )
            rel_key = parts[rel_col]
            rel_store[rel_key] = (
                rel_store[rel_key] + 1 if rel_key in rel_store else 1
            )
