import unittest 
import math
from constants import NOT_VISITED
from graphAlgos.astar import ASTAR

class TestAstar(unittest.TestCase):
    def test_no_weights(self):
        '''
        Tests basic functionality of Astar on a graph with no weights
        '''
        start = (0, 0)
        target = (5, 5)
        pickup = None
        grid = [[NOT_VISITED]*6 for _ in range(6)]
        weights = [[1]*6 for _ in range(6)]

        heuristic = lambda r,c: abs(target[0]-r) + abs(target[1]-c) #taxicab
        instance = ASTAR(start, target, pickup, grid, weights, heuristic)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()
        self.assertEqual(instance.shortest_path_length, 10)

        heuristic = lambda r,c: math.sqrt((target[0]-r)**2 + (target[1]-c)**2)
        instance = ASTAR(start, target, pickup, grid, weights, heuristic)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()
        self.assertEqual(instance.shortest_path_length, 10)

    def test_weights(self):
        '''
        Tests Astar functionality on a weighted graph
        '''
        start = (0, 0)
        target = (3, 3)
        pickup = None
        grid = [[NOT_VISITED]*4 for _ in range(4)]
        weights =  [[1, 2, 4, 5],
                    [2, 1, 1, 8],
                    [6, 4, 2, 4],
                    [8, 9, 4, 1]]

        heuristic = lambda r,c: abs(target[0]-r) + abs(target[1]-c) #taxicab
        instance = ASTAR(start, target, pickup, grid, weights, heuristic)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()
        # print(instance.grid)
        self.assertEqual(instance.shortest_path_length, 11)

        heuristic = lambda r,c: math.sqrt((target[0]-r)**2 + (target[1]-c)**2)
        instance = ASTAR(start, target, pickup, grid, weights, heuristic)
        instance.finding_shortest_path = True
        while instance.finding_shortest_path:
            instance.one_step()
        # print(instance.grid)
        self.assertEqual(instance.shortest_path_length, 11)

if __name__ == '__main__':
    unittest.main()