import unittest 
from constants import NOT_VISITED
from graphAlgos.bellmanFord import BELLMANFORD

class TestBellmanFord(unittest.TestCase):
    def test_no_weights(self):
        '''
        Tests basic functionality of Bellman Ford on a graph with no weights
        as well as the new_target functionality
        '''
        start = (0, 0)
        target = (5, 5)
        pickup = None
        grid = [[NOT_VISITED]*6 for _ in range(6)]
        weights = [[1]*6 for _ in range(6)]

        instance = BELLMANFORD(start, target, pickup, grid, weights)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()
        self.assertEqual(instance.shortest_path_length, 10)

        instance.new_target((5, 0))
        self.assertEqual(instance.shortest_path_length, 5)

    def test_source_is_target(self):
        start = (3, 3)
        target = (3, 3)
        pickup = None
        grid = [[NOT_VISITED]*6 for _ in range(6)]
        weights = [[1]*6 for _ in range(6)]

        instance = BELLMANFORD(start, target, pickup, grid, weights)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()
        self.assertEqual(instance.shortest_path_length, 0)

        # instance.new_target((5, 0))
        # self.assertEqual(instance.shortest_path_length, 5)

    # def test_weights(self):
    #     start = (3, 3)
    #     target = (5, 5)
    #     pickup = None
    #     grid = [[NOT_VISITED]*6 for _ in range(6)]
    #     weights = [[]]

    #     instance = BELLMANFORD(start, target, pickup, grid, weights)
    #     instance.finding_shortest_path = True
    #     while instance.finding_shortest_path:
    #         instance.one_step()
    #     self.assertEqual(instance.shortest_path_length, 10)

    #     instance.new_target((5, 0))
    #     self.assertEqual(instance.shortest_path_length, 5)

    def test_negative_cycle(self):
        pass
