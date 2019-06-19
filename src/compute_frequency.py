import argparse
import tempfile
import os
import sys

import shutil
import shelve

import utils

def main():
  parser = argparse.ArgumentParser(
    description='Compute the frequency of each entity and relation of a multi-relational graph'
  )
  parser.add_argument(
    'edgelist',
    help='Path of the edgelist file'
  )
  parser.add_argument(
    '-ef', '--ent-freq',
    default='entities_frequency.tsv',
    help='Output path of the frequency file for entities'
  )
  parser.add_argument(
    '-rf', '--rel-freq',
    default='relations_frequency.tsv',
    help='Output path of the frequency file for relations'
  )
  parser.add_argument(
    '-nh', '--no-header',
    type=bool,
    default=False,
    help='If you pass this the first line of the edgelist will be ignored'
  )
  args = parser.parse_args()

  edgelist_path = os.path.realpath(args.edgelist)
  ent_freq_path = os.path.realpath(args.ent_freq)
  rel_freq_path = os.path.realpath(args.rel_freq)

  if not os.path.isfile(edgelist_path):
    print('The edgelist file does not exists')
    sys.exit(1)

  with tempfile.TemporaryDirectory() as tmp:
    ent_dict_path = os.path.join(tmp, 'ent')
    rel_dict_path = os.path.join(tmp, 'rel')

    with shelve.open(ent_dict_path) as ent_dict,\
         shelve.open(rel_dict_path) as rel_dict:

      print('Computing the frequencies for entities and relations')
      with open(args.edgelist, 'r') as el:
        utils.frequencies_from_edgelist(
          edgelist=el,
          delimiter='\t',
          lhs_store=ent_dict,
          rhs_store=ent_dict,
          rel_store=rel_dict,
          lhs_col=0,
          rhs_col=2,
          rel_col=1,
          has_header=args.no_header
        )

      print('Writing the frequency file for entities')
      if not os.path.exists(os.path.dirname(ent_freq_path)):
        os.makedirs(os.path.dirname(ent_freq_path))
      with open(ent_freq_path, 'w+') as f:
        for ent in ent_dict:
          f.write('%s\t%d\n' % (ent, ent_dict[ent]))

      print('Writing the frequency file for relations')
      if not os.path.exists(os.path.dirname(rel_freq_path)):
        os.makedirs(os.path.dirname(rel_freq_path))
      with open(rel_freq_path, 'w+') as f:
        for rel in rel_dict:
          f.write('%s\t%d\n' % (rel, rel_dict[rel]))

      print('Sorting the frequency file for entities')
      utils.sort_file(
        ent_freq_path,
        delimiter='\t',
        columns=[1],
        has_header=False,
        reverse=True
      )

      print('Sorting the frequency file for relations')
      utils.sort_file(
        rel_freq_path,
        delimiter='\t',
        columns=[1],
        has_header=False,
        reverse=True
      )

if __name__ == '__main__':
  main()
