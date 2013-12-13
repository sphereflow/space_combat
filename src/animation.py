from billboard import *
import timer as Timer
import img_loader
from OpenGL.GL import *
import render_queue as RenderQueue

class Animation ( Billboard ) :
   def __init__(self) :
      super().__init__()
      self.looping = False
      self.self_destruct = False
      self.cur_frame = 0
      self.num_frames = 0
      self.st = Timer.SubTimer()

   def render(self) :
      glMatrixMode(GL_TEXTURE)
      npi = self.st.get_num_passed_intervals()
      self.cur_frame += npi
      if self.cur_frame > self.num_frames :
         if self.looping :
            self.cur_frame = self.cur_frame % self.num_frames
         else :
            if self.self_destruct :
               RenderQueue.dequeue(self)
      glLoadIdentity()
      glScalef(1.0 / self.num_frames, 1.0, 1.0)
      glTranslatef(self.cur_frame, 0.0, 0.0)
      glMatrixMode(GL_MODELVIEW)
      super().render()
      glMatrixMode(GL_TEXTURE)
      glLoadIdentity()
      glMatrixMode(GL_MODELVIEW)

   def copy(self) :
      c = Animation()
      c.looping = self.looping
      c.self_destruct = self.self_destruct
      c.set_texture(self.tex)
      c.m.r.width = self.m.r.width
      c.m.r.height = self.m.r.height
      c.num_frames = self.num_frames
      c.st.set_interval(self.st.get_interval())
      return c
