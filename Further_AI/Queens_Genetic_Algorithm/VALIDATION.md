# Validation

Checked on 11 October 2026 using Python 3.12.14 and NumPy 2.3.5 on Windows.

Command: `python -m unittest -v test_queens`

Result: **7 tests passed**, 25.218 seconds for the suite in this environment.

| Check | Coverage |
| --- | --- |
| Known boards | Valid classic and toroidal solutions; eight queens in one row produce 28 conflicts |
| Independent cost oracle | 400 generated boards across sizes 5, 7, 8 and 11; both classic and modular-arithmetic toroidal conflict counts |
| Neighbours | Correct board type, expected count, unique states, one changed queen and unchanged original board |
| Genetic operators | Crossover and forced mutation retain valid coordinates and preserve parents |
| Classic search | Seeds 0–4, each finds a zero-conflict solution within a 5,000-generation budget |
| Toroidal search | Size 7 with seeds 0–2 and size 11 with seed 0, each finds a zero-conflict solution within a 5,000-generation budget |
| Budget exhaustion | Size 8 stops after 20 generations and returns a board with conflicts |

The search answers are checked with an independent pairwise oracle rather than relying solely on the implementation's own `is_goal()` method. Both Python's and NumPy's random generators are seeded. Seeds support reproduction within a compatible environment; cross-version random behaviour is not guaranteed.

These are functional checks, not a statistical success-rate study, exhaustive proof, benchmark comparison or validation of every parameter combination.
