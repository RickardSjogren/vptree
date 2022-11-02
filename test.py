import unittest
import vptree
import numpy as np


class TestVPTree(unittest.TestCase):

    def test_single_nearest_neighbor(self):
        dim = 10
        query = [.5] * dim
        points, brute_force = brute_force_solution(20000, dim, query)
        tree = vptree.VPTree(points, euclidean)

        nearest = tree.get_nearest_neighbor(query)
        bf_nearest = brute_force[0]
        self.assertEqual(nearest[0], bf_nearest[0])
        self.assertTrue(all(n == b for n, b in zip(nearest[1], bf_nearest[1])))

    def test_nearest_neighbors(self):
        dim = 10
        query = [.5] * dim
        points, brute_force = brute_force_solution(20000, dim, query)
        tree = vptree.VPTree(points, euclidean)

        for k in (1, 10, len(points)):
            tree_nearest = tree.get_n_nearest_neighbors(query, k)
            self.assertEqual(len(tree_nearest), k)
            brute_force_nearest = brute_force[:k]
            for nearest, bf_nearest in zip(tree_nearest, brute_force_nearest):
                self.assertEqual(nearest[0], bf_nearest[0])
                self.assertTrue(all(n == b for n, b in zip(nearest[1],
                                                           bf_nearest[1])))

    def test_epsilon_search(self):
        dim = 10
        query = [.5] * dim
        points, brute_force = brute_force_solution(20000, dim, query)
        tree = vptree.VPTree(points, euclidean)

        for eps in (-1, 0, 1, 2, 10):
            tree_nearest = sorted(tree.get_all_in_range(query, eps))
            brute_force_nearest = [point for point in brute_force if
                                   point[0] < eps]
            for nearest, bf_nearest in zip(tree_nearest, brute_force_nearest):
                self.assertEqual(nearest[0], bf_nearest[0])
                self.assertTrue(all(n == b for n, b in zip(nearest[1],
                                                           bf_nearest[1])))

    def test_empty_points_raises_valueerror(self):
        self.assertRaises(ValueError, vptree.VPTree, [], euclidean)

    def test_zero_neighbors_raises_valueerror(self):
        tree = vptree.VPTree([1, 2, 3], euclidean)
        self.assertRaises(ValueError, tree.get_n_nearest_neighbors, [1], 0)

    def test_custom_points(self):
        points = [
            CustomPoint(0),
            CustomPoint(1),
            CustomPoint(2)
        ]

        tree = vptree.VPTree(points, custom_point_distance)

        test_point = CustomPoint(1)
        neighbors = tree.get_n_nearest_neighbors(test_point, 3)

        self.assertTrue(np.isclose(neighbors[0][0], 0))
        self.assertTrue(np.isclose(neighbors[0][1].x, 1))
        self.assertTrue(np.isclose(neighbors[1][0], 1))
        self.assertTrue(np.isclose(neighbors[2][0], 1))


def euclidean(p1, p2):
    return np.sqrt(np.sum(np.power(p2 - p1, 2)))


def brute_force_solution(n, dim, query, dist=euclidean):
    points = np.random.randn(n, dim)
    brute_force = [(dist(query, point), point) for point in points]
    brute_force.sort()

    return points, brute_force


class CustomPoint:
    def __init__(self, x: int):
        self.x = x


def custom_point_distance(cp_1: CustomPoint, cp_2: CustomPoint) -> float:
    return np.abs(cp_1.x - cp_2.x)


if __name__ == '__main__':
    unittest.main()
