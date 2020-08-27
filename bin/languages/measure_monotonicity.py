import argparse
from numpy import mean, float64
from pathos.multiprocessing import ProcessPool
from siminf import experiment_setups
from siminf import fileutil
from siminf import analysisutil
from siminf.fileutil import FileUtil

from siminf.languages import language_loader

def measure_monotonicity(languages):
    #return numpy.mean([float64(word.monotonicity) for word in language])
    from numpy import float64, mean
    mono_list = [float64(word.monotonicity) for word in languages]
    mean_value = mean(mono_list)
    return mean_value

def measure_monotonicity(monotonicity_list):
    from numpy import mean
    value = mean(monotonicity_list)
    return value

def main(args):
    setup = experiment_setups.parse(args.setup)
    dirname = fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name)
    file_util = FileUtil(dirname)
    #languages = language_loader.load_languages(file_util)
    languages = language_loader.load_all_evaluated_expressions(file_util) # to replace previous load logic
    monotonicity_list = [float64(word.monotonicity) for word in languages]
    
    print("args.processes={0}".format(args.processes))
    with ProcessPool(nodes=args.processes) as process_pool:
        # monotonicities = process_pool.map(measure_monotonicity, languages)
        monotonicities = process_pool.map(measure_monotonicity, monotonicity_list)

    file_util.dump_dill(monotonicities, 'monotonicity.dill')

    print("measure_monotonicity.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze")
    #common arguments
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--max_quantifier_length', type=int, required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--dest_dir', default='results')
    parser.add_argument('--processes', default=4, type=int)
    parser.add_argument('--name', default='run_0')
    #parse args
    args = parser.parse_args()
    main(args)