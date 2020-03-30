import argparse
import difflib
import os
import tempfile

from edgelist_mapper.bin.run import main as run_main

FIXTURE_PATH = os.path.realpath("tests/.fixtures")


def get_file_diffs(file1, file2):
    text1 = open(file1).readlines()
    text2 = open(file2).readlines()
    return list(difflib.unified_diff(text1, text2))


def test_main():
    cities_fixture = os.path.join(FIXTURE_PATH, "cities-s1")
    with tempfile.TemporaryDirectory() as tmp:
        args_edgelist_mapper = argparse.Namespace(
            edgelist=os.path.join(cities_fixture, "edgelist.tsv"), output=tmp,
        )
        run_main(args_edgelist_mapper)

        diffs = get_file_diffs(
            os.path.join(cities_fixture, "relations_frequency.tsv"),
            os.path.join(tmp, "relations_frequency.tsv"),
        )
        if len(diffs) > 0:
            print("Diffs in the relations_frequency.tsv files")
        for line in diffs:
            print(line, end="")
        assert len(diffs) == 0

        diffs = get_file_diffs(
            os.path.join(cities_fixture, "entities_frequency.tsv"),
            os.path.join(tmp, "entities_frequency.tsv"),
        )
        if len(diffs) > 0:
            print("Diffs in the entities_frequency.tsv files")
        for line in diffs:
            print(line, end="")
        assert len(diffs) == 0

        diffs = get_file_diffs(
            os.path.join(cities_fixture, "entities_mapping.tsv"),
            os.path.join(tmp, "entities_mapping.tsv"),
        )
        if len(diffs) > 0:
            print("Diffs in the entities_mapping.tsv files")
        for line in diffs:
            print(line, end="")
        assert len(diffs) == 0

        diffs = get_file_diffs(
            os.path.join(cities_fixture, "relations_mapping.tsv"),
            os.path.join(tmp, "relations_mapping.tsv"),
        )
        if len(diffs) > 0:
            print("Diffs in the relations_mapping.tsv files")
        for line in diffs:
            print(line, end="")
        assert len(diffs) == 0

        diffs = get_file_diffs(
            os.path.join(cities_fixture, "entities_mapping.tsv"),
            os.path.join(tmp, "entities_mapping.tsv"),
        )
        if len(diffs) > 0:
            print("Diffs in the entities_mapping.tsv files")
        for line in diffs:
            print(line, end="")
        assert len(diffs) == 0

        diffs = get_file_diffs(
            os.path.join(cities_fixture, "mapped_edgelist.tsv"),
            os.path.join(tmp, "mapped_edgelist.tsv"),
        )
        if len(diffs) > 0:
            print("Diffs in the mapped_edgelist.tsv files")
        for line in diffs:
            print(line, end="")
        assert len(diffs) == 0
