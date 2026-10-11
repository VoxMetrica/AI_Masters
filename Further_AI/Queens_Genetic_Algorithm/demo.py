"""Run a reproducible example without notebook state or external datasets."""
import argparse
import random
import numpy as np
from queens import GeneticAlgorithm, ToroidalGeneticAlgorithm

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--toroidal', type=int, metavar='N', help='use an N by N toroidal board (N >= 2)')
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--max-generations', type=int, default=5000)
args = parser.parse_args()
if args.max_generations < 1:
    parser.error('--max-generations must be positive')
if args.toroidal is not None and args.toroidal < 2:
    parser.error('--toroidal must be at least 2')
random.seed(args.seed)
np.random.seed(args.seed)
algorithm = (GeneticAlgorithm(max_gen=args.max_generations) if args.toroidal is None
             else ToroidalGeneticAlgorithm(n=args.toroidal, max_gen=args.max_generations))
answer, history = algorithm.run()
print(f'Rows by column: {answer.state.tolist()}')
print(f'Attacking pairs: {answer.cost()}; generations evaluated: {len(history)}')
print('Solved' if answer.is_goal() else 'Generation limit reached; returned board is not a solution')
