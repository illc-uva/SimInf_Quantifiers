import argparse
import os

from pathos.pools import ProcessPool

import Generator, ExperimentSetups

# Parameters
import fileutil
from fileutil import FileUtil

parser = argparse.ArgumentParser(description="Generate Quantifiers")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)

args = parser.parse_args()

processes = args.processes
setup = ExperimentSetups.parse(args.setup)
max_quantifier_length = args.max_quantifier_length
model_size = args.model_size

file_util = FileUtil(fileutil.base_dir(args.dest_dir, setup.name, max_quantifier_length, model_size))


universe = setup.generate_models(model_size)

folderName = "{0}/{1}_length={2}_size={3}".format(args.dest_dir,setup.name,max_quantifier_length,model_size)
os.makedirs("{0}".format(folderName), exist_ok=True)

processpool = ProcessPool(nodes=processes)
expression_generator = Generator.ExpressionGenerator(setup, model_size, universe, processpool)
(generated_expressions_dict, expressions_by_meaning) = \
    expression_generator.generate_all_expressions(max_quantifier_length)

print("{0} expressions!".format(len(expressions_by_meaning[bool].values())))

file_util.dump_dill(expressions_by_meaning[bool], 'generated_expressions.dill')
file_util.dump_dill(list(expressions_by_meaning[bool].values()), 'expressions.dill')
file_util.dump_dill(list(expressions_by_meaning[bool].keys()), 'meanings.dill')

processpool.close()
processpool.join()

print('Expression generation finished.')
