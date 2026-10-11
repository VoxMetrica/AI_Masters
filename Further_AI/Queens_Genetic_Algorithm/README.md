# Queens genetic algorithm

A completed Further AI coursework project exploring how a genetic algorithm can escape stagnation when solving the classic eight-queens puzzle and its toroidal-board extension.

The implementation combines tournament selection, single-point crossover, mutation, elitism and population resets after stagnation. The toroidal version changes the conflict calculation to account for wrapping across board edges and supports different board sizes.

## Run

From this directory, with Python 3.12:

```sh
python -m pip install -r requirements.txt
python demo.py --seed 0
python demo.py --toroidal 7 --seed 0
python -m unittest -v test_queens
```

The only runtime dependency is NumPy. No dataset, API key or notebook session is required. The dependency range is an installation constraint; the verified version is NumPy 2.3.5.

## Files

- [queens.py](queens.py): the final classic and toroidal implementations extracted from the coursework notebook.
- [demo.py](demo.py): a seeded command-line example added for this portfolio.
- [test_queens.py](test_queens.py): independent functional checks added for this portfolio.
- [report.pdf](report.pdf): the original five-page report, including design choices, recorded observations, comparison with particle swarm optimisation and references.
- [VALIDATION.md](VALIDATION.md): verification scope and results.

## Provenance and packaging

The source was `Further AI/eightqueens-ga/FurtherAI_GeneticAlgorithms.ipynb`: the board classes and final algorithms came from cells 5, 15, 20 and 21 (zero-based). The course supplied the original `EightQueensState` class, as acknowledged in the notebook. The coursework develops the genetic algorithms, stagnation reset strategy and toroidal extension. The original report discloses ChatGPT and GitHub Copilot assistance in code development.

For publication, final definitions were extracted into an importable module, avoiding the notebook's earlier experiments and later redefinition of the algorithm in its unused-approaches appendix. Two unused toroidal neighbour helpers were corrected to return `ToroidalQueensState` rather than `EightQueensState`; tests cover this correction. The search algorithm itself is unchanged. Documentation, the demo and tests were added with Codex assistance. Original local coursework files were preserved.

## Limitations

This is a stochastic educational implementation. The tested seeds found valid solutions, but neither a solution within a chosen generation budget nor a runtime bound is guaranteed. On exhaustion it returns the best member of the final population, which may still contain conflicts and need not be the best board seen across all resets. Always inspect `is_goal()` or `cost()`.

The algorithm classes expect sensible parameters, valid board values and a population at least as large as the tournament size; they are not hardened as a general-purpose library. The classic algorithm is specifically configured for eight queens. The toroidal implementation accepts other sizes, including cases with no solution.

The original report's timing observations are historical coursework results. The portfolio tests do not establish a universal sub-30-second guarantee or independently reproduce its full experiment. Its discussion of particle swarm optimisation is a literature comparison, not a PSO implementation or head-to-head benchmark. The report cites Hasançebi and Erbatur as 2024 in the body and 2000 in the bibliography; this citation inconsistency remains in the original PDF.
