from math_3d import *
from movement import *

class Kamera :
   screen_width = 0
   screen_height = 0
   projection = np.identity(4)
   mov = Movement()
   follow_movement = None
   forward_position = 0.0
   @staticmethod
   def set_rect(f) :
      x = f * Kamera.screen_width / Kamera.screen_height
      y = f
      if (x <= 0) or (y <= 0) :
         return
      Kamera.projection[0, 0] = 1.0 / x
      Kamera.projection[1, 1] = 1.0 / y
      Kamera.mov.r.width = x
      Kamera.mov.r.height = y

   @staticmethod
   def get_mpos() :
      r = Kamera.mov.get_mpos()
      fpos = np.array([0.0, Kamera.forward_position, 0.0, 0.0])
      fpos = np.dot(fpos, r)
      r[3, 0] -= fpos[0]
      r[3, 1] -= fpos[1]
      return r

   @staticmethod
   def follow(r) :
      Kamera.follow_movement = r

   @staticmethod
   def trigger() :
      if not Kamera.follow_movement :
         return
      Kamera.mov.r.pos = Kamera.follow_movement.r.pos.copy()
      Kamera.mov.r.pos[3] = 1.0
      Kamera.mov.r.angle = Kamera.follow_movement.r.angle * 1.0
