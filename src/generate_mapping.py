import argparse
import os
import sys

import shelve

import utils

def main():
  parser = argparse.ArgumentParser(
    description='Build a mapping from each named entity and relation of a multi-relational graph to an int'
  )
  parser.add_argument(
    '-ef', '--ent-freq',
    default='entities_frequency.tsv',
    help='Path of the frequency file for entities'
  )
  parser.add_argument(
    '-rf', '--rel-freq',
    default='relations_frequency.tsv',
    help='Path of the frequency file for relations'
  )
  parser.add_argument(
    '-rm', '--rel-map',
    default='relations_map.tsv',
    help='Output path of the mapping for entities'
  )
  parser.add_argument(
    '-em', '--ent-map',
    default='entities_map.tsv',
    help='Output path of the mapping for relations'
  )
  args = parser.parse_args()

  ent_freq_path = os.path.realpath(args.ent_freq)
  rel_freq_path = os.path.realpath(args.rel_freq)
  ent_map_path = os.path.realpath(args.ent_map)
  rel_map_path = os.path.realpath(args.rel_map)

  if not os.path.isfile(ent_freq_path):
    print('The entities frequency file does not exists')
    sys.exit(1)
  if not os.path.isfile(rel_freq_path):
    print('The relations frequency file does not exists')
    sys.exit(1)

  print('Writing the mapping file for entities')
  if not os.path.exists(os.path.dirname(ent_map_path)):
    os.makedirs(os.path.dirname(ent_map_path))
  with open(ent_map_path, 'w+') as em:
    with open(ent_freq_path, 'r') as ef:
      for idx, line in enumerate(ef):
        parts = line.rstrip('\n').split('\t', 1)
        em.write(str(idx) + '\t' + parts[0] + '\n')

  print('Writing the mapping file for relations')
  if not os.path.exists(os.path.dirname(rel_map_path)):
    os.makedirs(os.path.dirname(rel_map_path))
  with open(rel_map_path, 'w+') as rm:
    with open(rel_freq_path, 'r') as rf:
      for idx, line in enumerate(rf):
        parts = line.rstrip('\n').split('\t', 1)
        rm.write(str(idx) + '\t' + parts[0] + '\n')


if __name__ == '__main__':
  main()
