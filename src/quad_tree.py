from math_3d import *

# the root position will allways be (0, 0)
# subs allways contain full rects
# so the "big" rects are in the root node
# so are the rects positioned in the middle
class QuadTree :
   def __init__(self) :
      self.subs = []
      self.rects = []
      self.threshold = 3

   def insert(self, rect) :
      pass

   def remove(self, rect) :
      pass

   def subdivide(self) :
      pass

   def merge(self) :
      pass

   # returns a list of rects
   def get_collisions(self, rect) :
      pass

   # Action behaviour to update the QuadTree
   def perform(self) :
      pass
      # for each rect check if it is out of the root rectangles bounds
         # if so double root size, cache level 2 nodes,
         # insert 4 new level 2 nodes, insert cached nodes into level 3
         # + empty level 3 nodes
      # check if any rectangle is not fully covered anymore
      # if so reinsert
