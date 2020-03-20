import argparse
import difflib
import os
import tempfile

from main.bin.run import main as run_main

FIXTURE_PATH = os.path.realpath("src/tests/.fixtures")


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
            os.path.join(cities_fixture, "entities_mapping.tsv"),
            os.path.join(tmp, "entities_mapping.tsv"),
        )
        for line in diffs:
            print(line)
        assert len(diffs) == 0

        diffs = get_file_diffs(
            os.path.join(cities_fixture, "entities_mapping.tsv"),
            os.path.join(tmp, "entities_mapping.tsv"),
        )
        for line in diffs:
            print(line)
        assert len(diffs) == 0

        diffs = get_file_diffs(
            os.path.join(cities_fixture, "relations_mapping.tsv"),
            os.path.join(tmp, "relations_mapping.tsv"),
        )
        for line in diffs:
            print(line)
        assert len(diffs) == 0
