import numpy as np
import numpy.linalg as npla
from numpy import matrix
import math

class An :
   def __init__(self) :
      self.val = 0.0

   def copy(self) :
      r = An()
      r.val = self.val
      return r

   def get_degrees(self) :
      return self.val * 360.0 / (2.0 * math.pi)

   def set_degrees(self, f) :
      self.val = (f * 2.0 * math.pi / 360.0) % (2.0 * math.pi)

   def __add__(self, a) :
      ret = An()
      ret.val = self.val + a.val
      if ret.val >= 2.0 * math.pi :
         ret.val -= 2.0 * math.pi
      if ret.val < 0.0 :
         ret.val += 2.0 * math.pi
      return ret

   def __sub__(self, a) :
      ret = An()
      ret.val = self.val - a.val
      if ret.val >= 2.0 * math.pi :
         ret.val -= 2.0 * math.pi
      if ret.val < 0.0 :
         ret.val += 2.0 * math.pi
      return ret

   def __mul__(self, f) :
      ret = An()
      ret.val = self.val
      ret.val *= f
      if ret.val > 0.0 :
         ret.val -= 360.0 * math.floor(ret.val / 360.0)
      else :
         ret.val += 360.0 * math.ceil(ret.val / 360.0)
      return ret

def set_matrix_position(m, v) :
   m[3, 0] = v[0]
   m[3, 1] = v[1]

def set_matrix_position_val(m, x, y) :
   m[3, 0] = x
   m[3, 1] = y

def set_matrix_rotation(m, a) :
   m[1, 1] = m[0, 0] = math.cos(a.val)
   m[1, 0] = math.sin(a.val)
   m[0, 1] = -m[1, 0]

class Rect :
   mbuf = np.identity(4)
   mrbuf = np.identity(4)
   mpbuf = np.identity(4)
   posbuf = np.array([0.0, 0.0, 0.0, 1.0])
   def __init__(self) :
      self.angle = An()
      self.pos = np.array([0.0, 0.0, 0.0, 1.0])
      self.width = 1.0
      self.height = 1.0

   def get_modelview(self) :
      set_matrix_rotation(Rect.mbuf, self.angle)
      set_matrix_position(Rect.mbuf, self.pos)
      return Rect.mbuf

   def contains_vertex_of(self, r2) :
      rad2 = 1.5 * max(r2.width, r2.height)
      rad1 = 1.5 * max(self.width, self.height)
      diff = self.pos - r2.pos
      if (np.dot(diff, diff)) > ((rad1 + rad2) ** 2) :
         return False
      set_matrix_rotation(Rect.mrbuf, self.angle * -1)
      set_matrix_position_val(Rect.mpbuf, self.pos[0] * -1, self.pos[1] * -1)
      mv1inv = np.dot(Rect.mpbuf, Rect.mrbuf)
      mtrans = np.dot(r2.get_modelview(), mv1inv)
      p2 = np.array([r2.width, r2.height, 0, 2.0]) * 0.5
      for i in range(4):
         p2[3] = 1
         p = np.dot(p2, mtrans)
         p[3] = 1
         if (abs(p[0]) <= (self.width * 0.5)) and (abs(p[1]) <= (self.height * 0.5)) :
            return True
         if i == 0 :
            p2[0] *= -1
         if i == 1 :
            p2[1] *= -1
         if i == 2 :
            p2[0] *= -1
      return False
