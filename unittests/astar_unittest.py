import unittest 
import math
from constants import NOT_VISITED
from graphAlgos.astar import ASTAR

class TestAstar(unittest.TestCase):
    def test_no_weights(self):
        start = (0, 0)
        target = (5, 5)
        pickup = None
        grid = [[NOT_VISITED]*6 for _ in range(6)]
        weights = [[1]*6 for _ in range(6)]
        heuristic = lambda r,c: abs(target[0]-r) + abs(target[1]-c) #taxicab
        heuristic = lambda r,c: math.sqrt((target[0]-r)**2 + (target[1]-c)**2)
        instance = ASTAR(start, target, pickup, grid, weights, heuristic)
        instance.finding_shortest_path = True
        print(weights)
        while instance.finding_shortest_path or instance.drawing_shortest_path:
            instance.one_step()
            #print(self.grid)
           # print()
            #print("here")
        #self.assertEqual()
        print(instance.grid)
        self.assertEqual(instance.shortest_path_length, 10)

    # def weights(self):

if __name__ == '__main__':
    unittest.main()