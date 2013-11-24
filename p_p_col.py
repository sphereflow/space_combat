from collision import *
from math_3d import *
from b_b_col import *
from pixel_collidable import *

'''                     _   
      _______________  / \_
      |              |/    \__
      |              |        \__
      |             /|           /
      |            / |          /
      |           /_ |         /
      |_____________\_        /
                      \__    /
                         \__/

'''

class PPCol :
   def __init__(self) :
      pass

   def collides(self) :
      r1 = self.p_col1.r
      r2 = self.p_col2.r
      if not (r1.contains_vertex_of(r2) or r2.contains_vertex_of(r1)) :
         return False
      s1 = self.p_col1.spm
      s2 = self.p_col2.spm
      rects1 = []
      rects2 = []
      pixel_width = r1.width / s1.width
      pixel_height = r1.height / s1.height
      mbuf = np.identity(4)
      set_matrix_rotation(mbuf, r1.angle)
      for i in range(s1.width) :
         for j in range(s1.height) :
            if s1.is_solid(i, j) :
               pr = Rect()
               pr.width = pixel_width
               pr.height = pixel_height
               pr.pos[0] = (i + 0.5) * pixel_width - 0.5 * r1.width
               pr.pos[1] = -(j + 0.5) * pixel_height + 0.5 * r1.height
               pr.pos = np.dot(pr.pos, mbuf)
               pr.pos += r1.pos
               pr.angle = r1.angle
               rects1.append(r1)
      pixel_width = r2.width / s2.width
      pixel_height = r2.height / s2.height
      mbuf = np.identity(4)
      set_matrix_rotation(mbuf, r2.angle)
      for i in range(s2.width) :
         for j in range(s2.height) :
            if s2.is_solid(i, j) :
               pr = Rect()
               pr.width = pixel_width
               pr.height = pixel_height
               pr.pos[0] = (i + 0.5) * pixel_width - 0.5 * r2.width
               pr.pos[1] = -(j + 0.5) * pixel_height + 0.5 * r2.height
               pr.pos = np.dot(pr.pos, mbuf)
               pr.pos += r2.pos
               pr.angle = r2.angle
               rects2.append(r2)
      for pr1 in rects1 :
         for pr2 in rects2 :
            if (pr1.contains_vertex_of(r2)) or (pr2.contains_vertex_of(pr1)) :
               return True
      return False
