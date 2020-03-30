<h1 align="center">
  <b>edgelist-mapper</b>
</h1>
<p align="center">
  <!-- Build -->
  <a href="https://github.com/simonepri/edgelist-mapper/actions?query=workflow%3Abuild">
    <img src="https://github.com/simonepri/edgelist-mapper/workflows/build/badge.svg?branch=master" alt="Build status" />
  </a>
  <br />
  <!-- Code style -->
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style" />
  </a>
  <!-- Linter -->
  <a href="https://github.com/PyCQA/pylint">
    <img src="https://img.shields.io/badge/linter-pylint-ce963f.svg" alt="Linter" />
  </a>
  <!-- Test runner -->
  <a href="https://github.com/pytest-dev/pytest">
    <img src="https://img.shields.io/badge/test%20runner-pytest-449bd6.svg" alt="Test runner" />
  </a>
  <!-- Build tool -->
  <a href="https://github.com/python-poetry/poetry">
    <img src="https://img.shields.io/badge/build%20system-poetry-4e5dc8.svg" alt="Build tool" />
  </a>
  <br />
  <!-- License -->
  <a href="https://github.com/simonepri/edgelist-mapper/tree/master/license">
    <img src="https://img.shields.io/github/license/simonepri/edgelist-mapper.svg" alt="Project license" />
  </a>
</p>
<p align="center">
  📊 Maps nodes and edges of a multi-relational graph to integer
</p>


## Synopsis

edgelist-mapper is a simple tool that reads an edge-list file representing a graph and maps each node and relation to integer.
The mapping assigned is such that entities and relations that appear more frequently in the graph are mapped to smaller numerical values.

This tool is particularly useful to pre-process some of the publicly available knowledge graph datasets that are often used for the machine learning task of [relation prediction][repo:NLP-progress->relation_prediction.md].


## Input format

The tool takes as input a file (`edgelist.tsv`) that represents a graph as tab-separated triples of the form `(head, relation, tail)` and generates three new files, namely `mapped_edgelist.tsv`, `entities_map.tsv`, and `relations_map.tsv`.

```
san_marino	locatedin	europe
belgium	locatedin	europe
russia	locatedin	europe
monaco	locatedin	europe
croatia	locatedin	europe
poland	locatedin	europe
```
> Example content of the `edgelist.tsv` file.

```
0	europe
1	san_marino
2	russia
3	poland
4	monaco
5	croatia
6	belgium
```
> Content of the `entities_map.tsv` generated from the `edgelist.tsv` file.

```
0	locatedin
```
> Content of the `relations_map.tsv` generated from the `edgelist.tsv` file.

```
1	0	0
6	0	0
2	0	0
4	0	0
5	0	0
3	0	0
```
> Content of the `mapped_edgelist.tsv` generated from the `edgelist.tsv` file.


## CLI Usage

The CLI takes the following positional arguments:
```
  edgelist    Path of the edgelist file
  output      Path of the output directory
```

Example usage:
```bash
pip install git+https://github.com/simonepri/edgelist-mapper
python -m edgelist_mapper.bin.run \
    edgelist.tsv \
    .
```
> NB: You need Python 3 to run the CLI.


## Showcase

This tool has been used to create [this collection of datasets][repo:datasets-knowledge-embedding].


## Authors

- **Simone Primarosa** - [simonepri][github:simonepri]

See also the list of [contributors][contributors] who participated in this project.


## License

This project is licensed under the MIT License - see the [license][license] file for details.



<!-- Links -->

[license]: https://github.com/simonepri/edgelist-mapper/tree/master/license
[contributors]: https://github.com/simonepri/edgelist-mapper/contributors

[github:simonepri]: https://github.com/simonepri

[repo:NLP-progress->relation_prediction.md]:https://github.com/sebastianruder/NLP-progress/blob/master/english/relation_prediction.md
[repo:datasets-knowledge-embedding]: https://github.com/simonepri/datasets-knowledge-embedding
