import argparse
import tempfile
import os
import sys

import shutil
import shelve

import utils

def main():
  parser = argparse.ArgumentParser(
    description='Map the entities and the relations of an edgelist'
  )
  parser.add_argument(
    'edgelist',
    help='Path of the edgelist file'
  )
  parser.add_argument(
    '-rm', '--ent-map',
    default='entities_map.tsv',
    help='Output path of the mapping for entities'
  )
  parser.add_argument(
    '-em', '--rel-map',
    default='relations_map.tsv',
    help='Output path of the mapping for relations'
  )
  parser.add_argument(
    '-me', '--mapped-edgelist',
    default='mapped_esdgelist.tsv',
    help='Output path of the mapped edgelist'
  )
  args = parser.parse_args()

  edgelist_path = os.path.realpath(args.edgelist)
  ent_map_path = os.path.realpath(args.ent_map)
  rel_map_path = os.path.realpath(args.rel_map)
  el_map_path = os.path.realpath(args.mapped_edgelist)

  if not os.path.isfile(edgelist_path):
    print('The edgelist file does not exists')
    sys.exit(1)
  if not os.path.isfile(ent_map_path):
    print('The entities mapping file does not exists')
    sys.exit(1)
  if not os.path.isfile(rel_map_path):
    print('The relations mapping file does not exists')
    sys.exit(1)


  with tempfile.TemporaryDirectory() as tmp:
    ent_dict_path = os.path.join(tmp, 'ent')
    rel_dict_path = os.path.join(tmp, 'rel')

    with shelve.open(ent_dict_path) as rel_dict,\
         shelve.open(rel_dict_path) as ent_dict:
      print('Processing entities mapping')
      with open(ent_map_path, 'r') as em:
        for line in em:
          parts = line.rstrip('\n').split('\t')
          ent_dict[parts[1]] = parts[0]

      print('Processing relations mapping')
      with open(rel_map_path, 'r') as rm:
        for line in rm:
          parts = line.rstrip('\n').split('\t')
          rel_dict[parts[1]] = parts[0]

      print('Writing the mapped edgelist')
      if not os.path.exists(os.path.dirname(el_map_path)):
        os.makedirs(os.path.dirname(el_map_path))
      with open(el_map_path, 'w+') as mel:
        with open(edgelist_path, 'r') as el:
          for line in el:
            parts = line.rstrip('\n').split('\t')
            mel.write(ent_dict[parts[0]] + '\t' + rel_dict[parts[1]] + '\t' + ent_dict[parts[2]] + '\n')

if __name__ == '__main__':
  main()
