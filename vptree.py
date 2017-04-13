""" This module contains an implementation of a Vantage Point-tree (VP-tree)."""
import numpy as np


class VPTree:

    """ VP-Tree data structure for efficient nearest neighbor search.

    The VP-tree is a data structure for efficient nearest neighbor
    searching and finds the nearest neighbor in O(log n)
    complexity given a tree constructed of n data points. Construction
    complexity is O(n log n).

    Parameters
    ----------
    points : Iterable
        Construction points.
    dist_fn : Callable
        Function taking to point instances as arguments and returning
        the distance between them.
    leaf_size : int
        Minimum number of points in leaves.
    """

    def __init__(self, points, dist_fn, leaf_size=1):
        self.left = None
        self.right = None
        self.median = None
        self.dist_fn = dist_fn

        if not len(points):
            raise ValueError('Points can not be empty.')

        # TODO: Better vantage point selection.
        vp_i = np.random.choice(len(points))
        self.vp = points[vp_i]
        points = np.delete(points, vp_i, axis=0)

        if len(points) < leaf_size:
            return

        # Choose division boundary at median of distances.
        distances = [self.dist_fn(self.vp, p) for p in points]
        self.median = np.median(distances)

        left_points = []
        right_points = []
        for point, distance in zip(points, distances):
            if distance >= self.median:
                right_points.append(point)
            else:
                left_points.append(point)

        if len(left_points) > 0:
            self.left = VPTree(points=left_points, dist_fn=self.dist_fn)

        if len(right_points) > 0:
            self.right = VPTree(points=right_points, dist_fn=self.dist_fn)

    def _is_leaf(self):
        return (self.left is None) and (self.right is None)

    def get_nearest_neighbor(self, query):
        """ Get single nearest neighbor.
        
        Parameters
        ----------
        query : Any
            Query point.

        Returns
        -------
        Any
            Single nearest neighbor.
        """
        return self.get_n_nearest_neighbors(query, n_neighbors=1)[0]

    def get_n_nearest_neighbors(self, query, n_neighbors):
        """ Get `n_neighbors` nearest neigbors to `query`
        
        Parameters
        ----------
        query : Any
            Query point.
        n_neighbors : int
            Number of neighbors to fetch.

        Returns
        -------
        list
            List of `n_neighbors` nearest neighbors.
        """
        if not isinstance(n_neighbors, int) or n_neighbors < 1:
            raise ValueError('n_neighbors must be strictly positive integer')
        neighbors = _AutoSortingList(max_size=n_neighbors)
        nodes_to_visit = [self]

        furthest_distance = np.inf

        while len(nodes_to_visit) > 0:
            node = nodes_to_visit.pop(0)
            if node is None:
                continue

            d = self.dist_fn(query, node.vp)
            if d < furthest_distance:
                neighbors.append((d, node.vp))
                furthest_distance, _ = neighbors[-1]

            if node._is_leaf():
                continue

            if d < node.median:
                if d < node.median + furthest_distance:
                    nodes_to_visit.append(node.left)
                if d >= node.median - furthest_distance:
                    nodes_to_visit.append(node.right)
            else:
                if d >= node.median - furthest_distance:
                    nodes_to_visit.append(node.right)
                if d < node.median + furthest_distance:
                    nodes_to_visit.append(node.left)
                    
        return list(neighbors)

    def get_all_in_range(self, query, max_distance):
        """ Find all neighbours within `max_distance`.

        Parameters
        ----------
        query : Any
            Query point.
        max_distance : float
            Threshold distance for query.

        Returns
        -------
        neighbors : list
            List of points within `max_distance`.

        Notes
        -----
        Returned neighbors are not sorted according to distance.
        """
        neighbors = list()
        nodes_to_visit = [self]

        while len(nodes_to_visit) > 0:
            node = nodes_to_visit.pop(0)
            if node is None:
                continue

            d = self.dist_fn(query, node.vp)
            if d < max_distance:
                neighbors.append((d, node.vp))

            if node._is_leaf():
                continue

            if d < node.median:
                if d < node.median + max_distance:
                    nodes_to_visit.append(node.left)
                if d >= node.median - max_distance:
                    nodes_to_visit.append(node.right)
            else:
                if d >= node.median - max_distance:
                    nodes_to_visit.append(node.right)
                if d < node.median + max_distance:
                    nodes_to_visit.append(node.left)
        return neighbors


class _AutoSortingList(list):

    """ Simple auto-sorting list.

    Inefficient for large sizes since the queue is sorted at
    each push.

    Parameters
    ---------
    size : int, optional
        Max queue size.
    """

    def __init__(self, max_size=None, *args):
        super(_AutoSortingList, self).__init__(*args)
        self.max_size = max_size

    def append(self, item):
        """ Append `item` and sort.

        Parameters
        ----------
        item : Any
            Input item.
        """
        super(_AutoSortingList, self).append(item)
        self.sort()
        if self.max_size is not None and len(self) > self.max_size:
            self.pop()

