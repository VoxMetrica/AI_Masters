"""Independent checks for the coursework implementation."""
import contextlib
import io
import random
import unittest
import numpy as np
from queens import EightQueensState, ToroidalQueensState, GeneticAlgorithm, ToroidalGeneticAlgorithm


def conflicts(rows, toroidal=False):
    n = len(rows)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            dr, dc = int(rows[j]) - int(rows[i]), j - i
            attacked = dr == 0 or abs(dr) == dc
            if toroidal:
                attacked = dr % n == 0 or (dr - dc) % n == 0 or (dr + dc) % n == 0
            count += int(attacked)
    return count


class QueensTests(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        np.random.seed(42)

    def test_known_boards(self):
        self.assertEqual(EightQueensState(np.array([0, 4, 7, 5, 2, 6, 1, 3])).cost(), 0)
        self.assertEqual(EightQueensState(np.zeros(8, dtype=int)).cost(), 28)
        self.assertEqual(ToroidalQueensState(np.array([0, 2, 4, 6, 1, 3, 5])).cost(), 0)

    def test_cost_against_independent_oracle(self):
        for n in (5, 7, 8, 11):
            for _ in range(100):
                rows = np.random.randint(0, n, n)
                self.assertEqual(EightQueensState(rows).cost(), conflicts(rows))
                self.assertEqual(ToroidalQueensState(rows).cost(), conflicts(rows, True))

    def test_neighbours_preserve_board_type_and_original(self):
        for cls, n in ((EightQueensState, 8), (ToroidalQueensState, 7)):
            board = cls(n=n)
            original = board.state.copy()
            neighbours = board.neighbourhood()
            self.assertEqual(len(neighbours), n * (n - 1))
            self.assertEqual(len({tuple(x.state) for x in neighbours}), len(neighbours))
            for other in neighbours + [board.random_neighbour()]:
                self.assertIsInstance(other, cls)
                self.assertEqual(np.count_nonzero(other.state != original), 1)
                self.assertFalse(np.shares_memory(other.state, original))
            np.testing.assert_array_equal(board.state, original)

    def test_crossover_and_mutation_do_not_change_parents(self):
        for ga in (GeneticAlgorithm(), ToroidalGeneticAlgorithm(n=7)):
            a, b = ga.initialise_population()[:2]
            original_a, original_b = a.state.copy(), b.state.copy()
            child = ga.crossover(a, b)
            ga.mutation_rate = 1.0
            ga.mutate(child)
            self.assertEqual(child.n, a.n)
            self.assertTrue(np.all((child.state >= 0) & (child.state < child.n)))
            np.testing.assert_array_equal(a.state, original_a)
            np.testing.assert_array_equal(b.state, original_b)

    def test_seeded_classic_search(self):
        for seed in range(5):
            random.seed(seed)
            np.random.seed(seed)
            with contextlib.redirect_stdout(io.StringIO()):
                answer, record = GeneticAlgorithm(max_gen=5000).run()
            self.assertEqual(conflicts(answer.state), 0, f'seed {seed}')
            self.assertEqual(record[-1], 0)

    def test_seeded_toroidal_search(self):
        for n, seed in ((7, 0), (7, 1), (7, 2), (11, 0)):
            random.seed(seed)
            np.random.seed(seed)
            with contextlib.redirect_stdout(io.StringIO()):
                answer, record = ToroidalGeneticAlgorithm(n=n, max_gen=5000).run()
            self.assertEqual(conflicts(answer.state, True), 0, f'n={n}, seed={seed}')
            self.assertEqual(record[-1], 0)

    def test_unsolved_case_respects_generation_limit(self):
        with contextlib.redirect_stdout(io.StringIO()):
            answer, record = ToroidalGeneticAlgorithm(n=8, max_gen=20).run()
        self.assertEqual(len(record), 20)
        self.assertGreater(conflicts(answer.state, True), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
