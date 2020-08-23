import unittest 
from constants import NOT_VISITED
from graphAlgos.bfs import BFS

# python3 -m unittest unittests.bfs_unittest
class TestBFS(unittest.TestCase):
    def test_source_is_target(self):
        start = (3,3)
        target = (3,3)
        pickup = None
        grid = grid = [[NOT_VISITED]*6 for _ in range(6)]
        weights = [[1]*6 for _ in range(6)]

        instance = BFS(start, target, pickup, grid, weights)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()

        self.assertEqual(instance.shortest_path_length, 0)

    def test_change_target(self):
        start = (3,3)
        target = (3,5)
        pickup = None
        grid = grid = [[NOT_VISITED]*6 for _ in range(6)]
        weights = [[1]*6 for _ in range(6)]

        instance = BFS(start, target, pickup, grid, weights)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()

        self.assertEqual(instance.shortest_path_length, 2)

        instance.new_target((5,3))
        self.assertEqual(instance.shortest_path_length, 2)

        start = (3,3)
        target = (3,4)
        pickup = None
        grid = grid = [[NOT_VISITED]*6 for _ in range(6)]
        weights = [[1]*6 for _ in range(6)]

        instance = BFS(start, target, pickup, grid, weights)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()

        self.assertEqual(instance.shortest_path_length, 1)

        instance.new_target((3,5))
        self.assertEqual(instance.shortest_path_length, 2)
