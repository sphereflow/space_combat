from texture import *
import state_machine as StateMachine
from math_3d import *
from movement import *
from bound_collidable import *

class Billboard(BoundCollidable) :
   def __init__(self) :
      self.m = Movement()
      self.vbos = None
      self.list_index = -1
      self.vao = None

   def copy(self) :
      ret = Billboard()
      ret.set_texture(self.tex)
      ret.m.r.width = self.m.r.width
      ret.m.r.height = self.m.r.height
      return ret

   def render(self) :
      StateMachine.set_model_view(self.m.get_mpos())
      self.tex.set_tex()
      if self.vao != None :
         glBindVertexArray(self.vao)
         glDrawArrays(GL_TRIANGLES, 0, 4)
         return
      if self.vbos != None :
         glBindBuffer(GL_ARRAY_BUFFER, self.vbos[0])
         glVertexPointer(2, GL_FLOAT, 0, None)
         glBindBuffer(GL_ARRAY_BUFFER,self.vbos[1])
         glTexCoordPointer(2, GL_FLOAT, 0, None)
         glDrawArrays(GL_TRIANGLES, 0, 6)
         return
      if self.list_index >= 0 :
         glCallList(self.list_index)
         return
      glBegin(GL_TRIANGLES)
      glTexCoord2i(0, 1)
      glVertex2f(-self.m.r.width * 0.5, -self.m.r.height * 0.5)
      glTexCoord2i(1, 1)
      glVertex2f(self.m.r.width * 0.5, -self.m.r.height * 0.5)
      glTexCoord2i(1, 0)
      glVertex2f(self.m.r.width * 0.5, self.m.r.height * 0.5)
      glTexCoord2i(0, 1)
      glVertex2f(-self.m.r.width * 0.5, -self.m.r.height * 0.5)
      glTexCoord2i(1, 0)
      glVertex2f(self.m.r.width * 0.5, self.m.r.height * 0.5)
      glTexCoord2i(0, 0)
      glVertex2f(-self.m.r.width * 0.5, self.m.r.height * 0.5)
      glEnd()

   def get_rect(self, r) :
      r = self.m.r

   def set_texture(self, t) :
      if not t :
         return
      self.tex = t

   def get_texture(self) :
      return self.tex

   def gen_dl(self) :
      list_index = glGenLists(1)
      glNewList(list_index, GL_COMPILE)
      glBegin(GL_TRIANGLES)
      glTexCoord2i(0, 1)
      glVertex2f(-self.m.r.width * 0.5, -self.m.r.height * 0.5)
      glTexCoord2i(1, 1)
      glVertex2f(self.m.r.width * 0.5, -self.m.r.height * 0.5)
      glTexCoord2i(1, 0)
      glVertex2f(self.m.r.width * 0.5, self.m.r.height * 0.5)
      glTexCoord2i(0, 1)
      glVertex2f(-self.m.r.width * 0.5, -self.m.r.height * 0.5)
      glTexCoord2i(1, 0)
      glVertex2f(self.m.r.width * 0.5, self.m.r.height * 0.5)
      glTexCoord2i(0, 0)
      glVertex2f(-self.m.r.width * 0.5, self.m.r.height * 0.5)
      glEnd()
      glEndList()

   def gen_va(self) :
      self.vao = glGenVertexArrays(1)
      glBindVertexArray(self.vao)
      self.gen_vbo()
      glEnableVertexAttribArray(0)
      glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0)
      glEnableVertexAttribArray(1)
      glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, 0)
      # TODO : this sets the modelview, too. prevent this from happening

   def gen_vbo(self) :
      self.vbos = glGenBuffers(2) 
      d = np.array([-self.m.r.width * 0.5, -self.m.r.height * 0.5,
                     self.m.r.width * 0.5, -self.m.r.height * 0.5,
                     self.m.r.width * 0.5,  self.m.r.height * 0.5,
                    -self.m.r.width * 0.5, -self.m.r.height * 0.5,
                     self.m.r.width * 0.5,  self.m.r.height * 0.5,
                    -self.m.r.width * 0.5,  self.m.r.height * 0.5], dtype = 'float32')
      glBindBuffer(GL_ARRAY_BUFFER, self.vbos[0])
      glBufferData(GL_ARRAY_BUFFER, d, GL_STATIC_DRAW)
      d = np.array([0.0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0], dtype = 'float32')
      glBindBuffer(GL_ARRAY_BUFFER, self.vbos[1])
      glBufferData(GL_ARRAY_BUFFER, d, GL_STATIC_DRAW)
