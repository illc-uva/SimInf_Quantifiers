import argparse

import ExperimentSetups
import fileutil
from Languages.LanguageGenerator import EvaluatedExpression, generate_all, generate_sampled
from fileutil import FileUtil

parser = argparse.ArgumentParser(description="Generate Quantifiers")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('max_words', type=int)
parser.add_argument('--sample', type=int, default=None)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)
parser.add_argument('--fixedwordcount', default=False, action="store_true")
parser.add_argument('--name', default='run_0')
parser.add_argument('-i','--indices', nargs='*')

args = parser.parse_args()

setup = ExperimentSetups.parse(args.setup)

file_util_out = FileUtil(fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name))
file_util_in = FileUtil(fileutil.base_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size))

unevaluated_expressions = file_util_in.load_dill('expressions.dill')

if args.indices is not None:
    index_sets = []
    for indices_name in args.indices:
        index_sets.append(set(file_util_in.load_dill('{0}_expression_indices.dill'.format(indices_name))))
    indices = set.intersection(*index_sets)
else:
    indices = range(len(unevaluated_expressions))

if args.sample is None:
    languages = generate_all(indices, args.max_words, args.fixedwordcount)
else:
    languages = generate_sampled(indices, args.max_words, args.sample, args.fixedwordcount)

file_util_out.dump_dill(languages, 'language_indices.dill')
file_util_out.save_stringlist([list(map(str, lang)) for lang in languages], 'languages.txt')
