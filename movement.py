from math_3d import *
from action import *
import timer as Timer

class Movement ( object ):
   mret = np.identity(4)
   def __init__(self) :
      self.sll = SlideLeft(self)
      self.slr = SlideRight(self)
      self.tl = TurnLeft(self)
      self.tr = TurnRight(self)
      self.fwd = Forward(self)
      self.bwd = Backward(self)
      self.r = Rect()
      self.sub_movements = []

   def get_mpos(self) :
      set_matrix_rotation(Movement.mret, self.r.angle)
      set_matrix_position(Movement.mret, self.r.pos)
      return Movement.mret

   def move_by(self, v) :
      self.r.pos += v
      self.r.pos[3] = 1.0
      for sm in self.sub_movements :
         sm.move_by(v)

   def turn_by(self, a) :
      self.r.angle += a
      for sm in self.sub_movements :
         sm.turn_by(a)

class AccMovement ( Movement ) :
   def __init__(self) :
      super().__init__()

class SlideLeft(Action) :
   def __init__(self, mov) :
      self.m = mov
      self.ups = 1.0

   def perform(self) :
      vbuf = np.array([-1.0, 0.0, 0.0, 1.0])
      mbuf = np.identity(4)
      set_matrix_rotation(mbuf, self.m.r.angle)
      vbuf = np.dot(vbuf, mbuf)
      vbuf *= self.ups * Timer.instance.frame_time()
      self.m.move_by(vbuf)

class SlideRight(Action) :
   def __init__(self, mov) :
       self.m = mov
       self.ups = 1.0

   def perform(self) :
      vbuf = np.array([1.0, 0.0, 0.0, 1.0])
      mbuf = np.identity(4)
      set_matrix_rotation(mbuf, self.m.r.angle)
      vbuf = np.dot(vbuf, mbuf)
      vbuf *= self.ups * Timer.instance.frame_time()
      self.m.move_by(vbuf)

class TurnLeft(Action) :
   def __init__(self, mov) :
      self.m = mov
      self.ups = 1.0

   def perform(self) :
      anbuf = An()
      anbuf.val = -Timer.instance.frame_time() * self.ups * 2 * math.pi
      self.m.turn_by(anbuf)

class TurnRight(Action) :
   def __init__(self, mov) :
      self.m = mov
      self.ups = 1.0

   def perform(self) :
      anbuf = An()
      anbuf.val = Timer.instance.frame_time() * self.ups * 2 * math.pi
      self.m.turn_by(anbuf)

class Forward(Action) :
   def __init__(self, mov) :
      self.m = mov
      self.ups = 1.0
      self.max_ups = 1.0
      self.acc = None

   def add_acceleration(self, ups) :
      self.acc = Acceleration(self)
      self.acc.ups = ups

   def perform(self) :
      mbuf = np.identity(4)
      set_matrix_rotation(mbuf, self.m.r.angle)
      vbuf = np.dot(np.array([0.0, 1.0, 0.0, 1.0]), mbuf)
      vbuf *= self.ups * Timer.instance.frame_time()
      self.m.move_by(vbuf)

class Backward(Action) :
   def __init__(self, mov) :
      self.m = mov
      self.ups = 1.0
      self.max_ups = 1.0
      self.acc = None

   def add_acceleration(self, ups) :
      self.acc = Acceleration(self)
      self.acc.ups = self.ups

   def perform(self) :
      mbuf = np.identity(4)
      set_matrix_rotation(mbuf, self.m.r.angle)
      vbuf = np.dot(np.array([0.0, -1.0, 0.0, 1.0]), mbuf)
      vbuf *= self.ups * Timer.instance.frame_time()
      self.m.move_by(vbuf)

# to move with acceleration call add_acceleration
# set max ups
# then enqueue accelerated movement in UpdateEvt
# bind acc to key/ mouse / whatever evt
class Acceleration(Action) :
   def __init__(self, parent) :
      self.ups = 1.0 # acceleration rate
      
   def perform(self) :
      self.parent.ups += self.ups
      if self.parent.ups > self.parent.max_ups :
         self.parent.ups = self.parent.max_ups
