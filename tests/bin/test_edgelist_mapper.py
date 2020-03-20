import argparse
import filecmp
import os
import tempfile

from bin.edgelist_mapper import main as edgelist_mapper_main

fixture_path = os.path.realpath("tests/.fixtures")

def test_main():
    cities_fixture = os.path.join(fixture_path, "cities-s1")
    with tempfile.TemporaryDirectory() as tmp:
        args_edgelist_mapper = argparse.Namespace(
            edgelist=os.path.join(cities_fixture, "edgelist.tsv"),
            output=tmp,
        )
        edgelist_mapper_main(args_edgelist_mapper)

        assert filecmp.cmp(
            os.path.join(cities_fixture, "entities_mapping.tsv"),
            os.path.join(tmp, "entities_mapping.tsv")
        ) == True

        assert filecmp.cmp(
            os.path.join(cities_fixture, "entities_mapping.tsv"),
            os.path.join(tmp, "entities_mapping.tsv")
        ) == True

        assert filecmp.cmp(
            os.path.join(cities_fixture, "relations_mapping.tsv"),
            os.path.join(tmp, "relations_mapping.tsv")
        ) == True
