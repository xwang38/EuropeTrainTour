#Copyright 2013, Michael H. Goldwasser (leave as is)

class Empty(Exception):
    """Error attempting to access an element from an empty container."""
    pass

class PriorityQueueBase:
  """Abstract base class for a priority queue."""

  #------------------------------ nested _Item class ------------------------------
  class _Item:
    """Lightweight composite to store priority queue items."""
    __slots__ = '_key', '_value'

    def __init__(self, k, v):
      self._key = k
      self._value = v

    def __lt__(self, other):
      return self._key < other._key    # compare items based on their keys

    def __repr__(self):
      return '({0},{1})'.format(self._key, self._value)

  #------------------------------ public behaviors ------------------------------
  def is_empty(self):                  # concrete method assuming abstract len
    """Return True if the priority queue is empty."""
    return len(self) == 0

  def __len__(self):
    """Return the number of items in the priority queue."""
    raise NotImplementedError('must be implemented by subclass')

  def add(self, key, value):
    """Add a key-value pair."""
    raise NotImplementedError('must be implemented by subclass')

  def min(self):
    """Return but do not remove (k,v) tuple with minimum key.

    Raise Empty exception if empty.
    """
    raise NotImplementedError('must be implemented by subclass')

  def remove_min(self):
    """Remove and return (k,v) tuple with minimum key.

    Raise Empty exception if empty.
    """
    raise NotImplementedError('must be implemented by subclass')

class HeapPriorityQueue(PriorityQueueBase): # base class defines _Item
  """A min-oriented priority queue implemented with a binary heap."""

  #------------------------------ nonpublic behaviors ------------------------------
  def _parent(self, j):
    return (j-1) // 2

  def _left(self, j):
    return 2*j + 1

  def _right(self, j):
    return 2*j + 2

  def _has_left(self, j):
    return self._left(j) < len(self._data)     # index beyond end of list?

  def _has_right(self, j):
    return self._right(j) < len(self._data)    # index beyond end of list?

  def _swap(self, i, j):
    """Swap the elements at indices i and j of array."""
    self._data[i], self._data[j] = self._data[j], self._data[i]

  def _upheap(self, j):
    parent = self._parent(j)
    if j > 0 and self._data[j] < self._data[parent]:
      self._swap(j, parent)
      self._upheap(parent)             # recur at position of parent

  def _downheap(self, j):
    if self._has_left(j):
      left = self._left(j)
      small_child = left               # although right may be smaller
      if self._has_right(j):
        right = self._right(j)
        if self._data[right] < self._data[left]:
          small_child = right
      if self._data[small_child] < self._data[j]:
        self._swap(j, small_child)
        self._downheap(small_child)    # recur at position of small child

  #------------------------------ public behaviors ------------------------------
  def __init__(self):
    """Create a new empty Priority Queue."""
    self._data = []

  def __len__(self):
    """Return the number of items in the priority queue."""
    return len(self._data)

  def add(self, key, value):
    """Add a key-value pair to the priority queue."""
    self._data.append(self._Item(key, value))
    self._upheap(len(self._data) - 1)            # upheap newly added position

  def min(self):
    """Return but do not remove (k,v) tuple with minimum key.

    Raise Empty exception if empty.
    """
    if self.is_empty():
      raise Empty('Priority queue is empty.')
    item = self._data[0]
    return (item._key, item._value)

  def remove_min(self):
    """Remove and return (k,v) tuple with minimum key.

    Raise Empty exception if empty.
    """
    if self.is_empty():
      raise Empty('Priority queue is empty.')
    self._swap(0, len(self._data) - 1)           # put minimum item at the end
    item = self._data.pop()                      # and remove it from the list;
    self._downheap(0)                            # then fix new root
    return (item._key, item._value)

class AdaptableHeapPriorityQueue(HeapPriorityQueue):
  """A locator-based priority queue implemented with a binary heap."""

  #------------------------------ nested Locator class ------------------------------
  class Locator(HeapPriorityQueue._Item):
    """Token for locating an entry of the priority queue."""
    __slots__ = '_index'                 # add index as additional field

    def __init__(self, k, v, j):
      super().__init__(k,v)
      self._index = j

  #------------------------------ nonpublic behaviors ------------------------------
  # override swap to record new indices
  def _swap(self, i, j):
    super()._swap(i,j)                   # perform the swap
    self._data[i]._index = i             # reset locator index (post-swap)
    self._data[j]._index = j             # reset locator index (post-swap)

  def _bubble(self, j):
    if j > 0 and self._data[j] < self._data[self._parent(j)]:
      self._upheap(j)
    else:
      self._downheap(j)

  #------------------------------ public behaviors ------------------------------
  def add(self, key, value):
    """Add a key-value pair."""
    token = self.Locator(key, value, len(self._data)) # initiaize locator index
    self._data.append(token)
    self._upheap(len(self._data) - 1)
    return token

  def update(self, loc, newkey, newval):
    """Update the key and value for the entry identified by Locator loc."""
    j = loc._index
    if not (0 <= j < len(self) and self._data[j] is loc):
      raise ValueError('Invalid locator')
    loc._key = newkey
    loc._value = newval
    self._bubble(j)

  def remove(self, loc):
    """Remove and return the (k,v) pair identified by Locator loc."""
    j = loc._index
    if not (0 <= j < len(self) and self._data[j] is loc):
      raise ValueError('Invalid locator')
    if j == len(self) - 1:                # item at last position
      self._data.pop()                    # just remove it
    else:
      self._swap(j, len(self)-1)          # swap item to the last position
      self._data.pop()                    # remove it from the list
      self._bubble(j)                     # fix item displaced by the swap
    return (loc._key, loc._value)

  def get(self,loc):
      return (loc._key, loc._value)

class shortest_path:

    def shortest_path_lengths(self, g, src):
      """Compute shortest-path distances from src to reachable vertices of g.

      Graph g can be undirected or directed, but must be weighted such that
      e.element() returns a numeric weight for each edge e.

      Return dictionary mapping each reachable vertex to its distance from src.
      """
      d = {}                                        # d[v] is upper bound from s to v
      cloud = {}                                    # map reachable v to its d[v] value
      pq = AdaptableHeapPriorityQueue()             # vertex v will have key d[v]
      pqlocator = {}                                # map from vertex to its pq locator

      # for each vertex v of the graph, add an entry to the priority queue, with
      # the source having distance 0 and all others having infinite distance
      for v in g.vertices():
        if v is src:
          d[v] = 0
        else:
          d[v] = float('inf')                       # syntax for positive infinity
        pqlocator[v] = pq.add(d[v], v)              # save locator for future updates

      while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key                              # its correct d[u] value
        del pqlocator[u]                            # u is no longer in pq
        for e in g.incident_edges(u):               # outgoing edges (u,v)
          v = e.opposite(u)
          if v not in cloud:
            # perform relaxation step on edge (u,v)
            wgt = e.element()
            if d[u] + wgt < d[v]:                   # better path to v?
              d[v] = d[u] + wgt                     # update the distance
              pq.update(pqlocator[v], d[v], v)      # update the pq entry

      return cloud                                  # only includes reachable vertices

    def shortest_path_tree(self, g, s, d):
      """Reconstruct shortest-path tree rooted at vertex s, given distance map d.

      Return tree as a map from each reachable vertex v (other than s) to the
      edge e=(u,v) that is used to reach v from its parent u in the tree.
      """
      tree = {}
      for v in d:
        if v is not s:
          for e in g.incident_edges(v, False):       # consider INCOMING edges
            u = e.opposite(v)
            wgt = e.element()
            if d[v] == d[u] + wgt:
              tree[v] = e                            # edge e is used to reach v
      return tree
