import collision
import bound_colidable
import math_3d

class BBCol :
   def __init__(self) :
      pass

   def collides(self) :
      self.b1.get_rect(r1)
      self.b2.get_rect(r2)
      return r1.contains_vertex_of(r2) or r2.contains_vertex_of(r1)
