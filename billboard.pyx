import texture
import state_machine as StateMachine
from math_3d import *
from movement import *
from bound_collidable import *
import OpenGL.GL as GL
cdef extern from "GL/gl.h" :
   ctypedef int GLint
   ctypedef int GLsizei
   ctypedef void GLvoid
   ctypedef unsigned int GLuint
   ctypedef unsigned int GLenum
   cdef void glEnd()
   cdef void glCallList(GLuint l)
   cdef void glBindBuffer(GLenum target, GLuint b)
   cdef void glVertexPointer(GLint size, GLenum t, GLsizei stride, const GLvoid * pointer)
   cdef void glTexCoordPointer(GLint size, GLenum t, GLsizei stride, const GLvoid * pointer)
   cdef void glDrawArrays(GLenum mode, GLint first, GLsizei count)

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
         GL.glBindVertexArray(self.vao)
         GL.glDrawArrays(GL.GL_TRIANGLES, 0, 4)
         return
      if self.vbos != None :
         glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbos[0])
         glVertexPointer(2, GL.GL_FLOAT, 0, NULL)
         glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbos[1])
         glTexCoordPointer(2, GL.GL_FLOAT, 0, NULL)
         glDrawArrays(GL.GL_TRIANGLES, 0, 6)
         return
      if self.list_index >= 0 :
         glCallList(self.list_index)
         return
      GL.glBegin(GL.GL_TRIANGLES)
      GL.glTexCoord2i(0, 1)
      GL.glVertex2f(-self.m.r.width * 0.5, -self.m.r.height * 0.5)
      GL.glTexCoord2i(1, 1)
      GL.glVertex2f(self.m.r.width * 0.5, -self.m.r.height * 0.5)
      GL.glTexCoord2i(1, 0)
      GL.glVertex2f(self.m.r.width * 0.5, self.m.r.height * 0.5)
      GL.glTexCoord2i(0, 1)
      GL.glVertex2f(-self.m.r.width * 0.5, -self.m.r.height * 0.5)
      GL.glTexCoord2i(1, 0)
      GL.glVertex2f(self.m.r.width * 0.5, self.m.r.height * 0.5)
      GL.glTexCoord2i(0, 0)
      GL.glVertex2f(-self.m.r.width * 0.5, self.m.r.height * 0.5)
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
      list_index = GL.glGenLists(1)
      GL.glNewList(list_index, GL.GL_COMPILE)
      GL.glBegin(GL.GL_TRIANGLES)
      GL.glTexCoord2i(0, 1)
      GL.glVertex2f(-self.m.r.width * 0.5, -self.m.r.height * 0.5)
      GL.glTexCoord2i(1, 1)
      GL.glVertex2f(self.m.r.width * 0.5, -self.m.r.height * 0.5)
      GL.glTexCoord2i(1, 0)
      GL.glVertex2f(self.m.r.width * 0.5, self.m.r.height * 0.5)
      GL.glTexCoord2i(0, 1)
      GL.glVertex2f(-self.m.r.width * 0.5, -self.m.r.height * 0.5)
      GL.glTexCoord2i(1, 0)
      GL.glVertex2f(self.m.r.width * 0.5, self.m.r.height * 0.5)
      GL.glTexCoord2i(0, 0)
      GL.glVertex2f(-self.m.r.width * 0.5, self.m.r.height * 0.5)
      glEnd()
      GL.glEndList()

   def gen_va(self) :
      self.vao = glGenVertexArrays(1)
      GL.glBindVertexArray(self.vao)
      self.gen_vbo()
      GL.glEnableVertexAttribArray(0)
      GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, 0)
      GL.glEnableVertexAttribArray(1)
      GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, 0)
      # TODO : this sets the modelview, too. prevent this from happening

   def gen_vbo(self) :
      self.vbos = GL.glGenBuffers(2) 
      d = np.array([-self.m.r.width * 0.5, -self.m.r.height * 0.5,
                     self.m.r.width * 0.5, -self.m.r.height * 0.5,
                     self.m.r.width * 0.5,  self.m.r.height * 0.5,
                    -self.m.r.width * 0.5, -self.m.r.height * 0.5,
                     self.m.r.width * 0.5,  self.m.r.height * 0.5,
                    -self.m.r.width * 0.5,  self.m.r.height * 0.5], dtype = 'float32')
      glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbos[0])
      GL.glBufferData(GL.GL_ARRAY_BUFFER, d, GL.GL_STATIC_DRAW)
      d = np.array([0.0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0], dtype = 'float32')
      glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbos[1])
      GL.glBufferData(GL.GL_ARRAY_BUFFER, d, GL.GL_STATIC_DRAW)
