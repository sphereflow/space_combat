from cython.view cimport array as cvarray
cimport cython
cimport numpy as np
import numpy as np
import numpy.linalg as npla
from numpy import matrix
import math
from libc.math cimport sin, cos, floor, ceil, sqrt, M_PI, M_1_PI

DTYPE = np.double
ctypedef np.double_t DTYPE_t

cdef class An :
   cdef public double val
   def __init__(self) :
      self.val = 0.0

   def copy(self) :
      r = An()
      r.val = self.val
      return r

   cpdef double get_degrees(self) :
      return self.val * 360.0 * 0.5 * M_1_PI

   def set_degrees(self, double f) :
      self.val = (f * 2.0 * M_PI / 360.0) % (2.0 * M_PI)

   @cython.boundscheck(False)
   def rotate(self, np.ndarray[DTYPE_t, ndim = 1] v) :
      cdef np.ndarray[DTYPE_t, ndim = 1] r = np.zeros(4)
      cdef double s = sin(self.val)
      cdef double c = cos(self.val)
      r[0] = c * v[0] + s * v[1]
      r[1] = -s * v[0] + c * v[1]
      r[3] = 1.0
      return r

   def __add__(self, An a) :
      ret = An()
      ret.val = self.val + a.val
      if ret.val >= 2.0 * M_PI :
         ret.val -= 2.0 * M_PI
      if ret.val < 0.0 :
         ret.val += 2.0 * M_PI
      return ret

   def __sub__(self, An a) :
      ret = An()
      ret.val = self.val - a.val
      if ret.val >= 2.0 * M_PI :
         ret.val -= 2.0 * M_PI
      if ret.val < 0.0 :
         ret.val += 2.0 * M_PI
      return ret

   def __mul__(self, double f) :
      ret = An()
      ret.val = self.val
      ret.val *= f
      if ret.val > 0.0 :
         ret.val -= 360.0 * floor(ret.val / 360.0)
      else :
         ret.val += 360.0 * ceil(ret.val / 360.0)
      return ret

@cython.boundscheck(False)
def set_matrix_position(np.ndarray m, np.ndarray v) :
   cdef double [:, :] mv = m
   cdef double [:] vv = v
   mv[3, 0] = vv[0]
   mv[3, 1] = vv[1]

@cython.boundscheck(False)
def set_matrix_position_val(np.ndarray m, double x, double y) :
   cdef double [:, :] mv = m
   mv[3, 0] = x
   mv[3, 1] = y

@cython.boundscheck(False)
def set_matrix_rotation(np.ndarray[DTYPE_t, ndim = 2] m, An a) :
   cdef double [:, :] mv = m
   mv[1, 1] = mv[0, 0] = cos(a.val)
   mv[1, 0] = sin(a.val)
   mv[0, 1] = -mv[1, 0]

@cython.boundscheck(False)
def dot(np.ndarray[DTYPE_t, ndim = 1] v1, np.ndarray[DTYPE_t, ndim = 1] v2) :
   return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

@cython.boundscheck(False)
def length(np.ndarray[DTYPE_t, ndim = 1] v1) :
   return sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)

@cython.boundscheck(False)
@cython.cdivision(True)
def unit(np.ndarray[DTYPE_t, ndim = 1] v1) :
   cdef double sql = sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
   if sql == 0.0 :
      return v1.copy()
   cdef double f = 1.0 / sql
   return v1 * f

cdef class Rect :
   mbuf = np.identity(4)
   mrbuf = np.identity(4)
   mpbuf = np.identity(4)
   posbuf = np.array([0.0, 0.0, 0.0, 1.0])
   cdef public An angle
   cdef public np.ndarray pos
   cdef public double width
   cdef public double height
   def __init__(self) :
      self.angle = An()
      self.pos = np.zeros(4)
      self.pos[3] = 1.0
      self.width = 1.0
      self.height = 1.0

   def get_modelview(self) :
      set_matrix_rotation(Rect.mbuf, self.angle)
      set_matrix_position(Rect.mbuf, self.pos)
      return Rect.mbuf

   @cython.boundscheck(False)
   def contains_vertex_of(self, Rect r2) :
      cdef double rad2 = 1.5 * max(r2.width, r2.height)
      cdef double rad1 = 1.5 * max(self.width, self.height)
      cdef double x_diff = self.pos[0] - r2.pos[0]
      cdef double y_diff = self.pos[1] - r2.pos[1]
      if (x_diff ** 2 + y_diff ** 2) > ((rad1 + rad2) ** 2) :
         return False
      set_matrix_rotation(Rect.mrbuf, self.angle * -1)
      Rect.mpbuf[3, 0] = -self.pos[0]
      Rect.mpbuf[3, 1] = -self.pos[1]
      cdef np.ndarray[DTYPE_t, ndim = 2] mv1inv = np.dot(Rect.mpbuf, Rect.mrbuf)
      cdef np.ndarray[DTYPE_t, ndim = 2] mtrans = np.dot(r2.get_modelview(), mv1inv)
      cdef double [:, :] mtransv = mtrans
      p2 = np.array([r2.width, r2.height, 0, 2.0]) * 0.5
      cdef double [:] p2v = p2
      cdef np.ndarray[DTYPE_t, ndim = 1] p = np.zeros(4)
      cdef double [:] pv = p
      cdef int i, j, k
      for i in range(4):
         p2v[3] = 1.0
         #p = np.dot(p2v, mtransv)
         for j in range(4) :
            pv[j] = 0.0
            for k in range(4) :
               pv[j] += p2v[k] * mtransv[k, j]
         pv[3] = 1.0
         if (abs(pv[0]) <= (self.width * 0.5)) and (abs(pv[1]) <= (self.height * 0.5)) :
            return True
         if i == 0 :
            p2v[0] *= -1.0
         if i == 1 :
            p2v[1] *= -1.0
         if i == 2 :
            p2v[0] *= -1.0
      return False
