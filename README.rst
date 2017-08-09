VP-Tree
=======

This package contains an implementation of a `vantage-point tree <https://en.wikipedia.org/wiki/Vantage-point_tree>`_ data structure.

Installation
------------

Simply install through pip:

.. code-block::

  pip install vptree

Example
-------

Example usage:

.. code-block:: python

  import numpy as np
  import vptree
  
  # Define distance function.
  def euclidean(p1, p2):
    return np.sqrt(np.sum(np.power(p2 - p1, 2)))
  
  # Generate some random points.
  points = np.random.randn(20000, 10)
  query = [.5] * 10
  
  # Build tree in O(n log n) time complexity.
  tree = vptree.VPTree(points, euclidean)   
  
  # Query single point.
  tree.get_nearest_neighbor(query)
  
  # Query n-points.
  tree.get_n_nearest_neighbors(query, 10)
  
  # Get all points within certain distance.
  tree.get_all_in_range(query, 3.14)
