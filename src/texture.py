from OpenGL.GL import *
from image import *
from solid_pixel_map import *
from transparency_map import *

class Texture( Image ) :
   ntex = 0
   current_tex_num = -1
   def __init__(self) :
      super().__init__()
      self.tex_num = -1
      self.stage = 0
      self.ref_count = 0
      self.spm = None

   def prepare_image(self) :
      if self.tex_num != -1 :
         return
      Texture.ntex += 1
      print(Texture.ntex)
      self.tex_num = glGenTextures(1)
      glBindTexture(GL_TEXTURE_2D, self.tex_num)
      glActiveTexture(GL_TEXTURE0 + self.stage)
      # make the rendering pretty and smudgy and repeat texture if it is too small
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      # transfering the actual texture
      if self.is_transparent() :
         glTexImage2D(GL_TEXTURE_2D, self.stage, 4, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)
      else :
         glTexImage2D(GL_TEXTURE_2D, self.stage, 3, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.data)
      # some glTexEnv[if] calls
      glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
      #glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_COLOR, GL_REPLACE)

   def set_tex(self) :
      if Texture.current_tex_num == self.tex_num :
         return
      glBindTexture(GL_TEXTURE_2D, self.tex_num)
      glActiveTexture(GL_TEXTURE0 + self.stage)
      Texture.current_tex_num = self.tex_num

   def apply_transparency_map(self, m) :
      if not m :
         return
      if (m.height != self.height) or (m.width != self.width) :
         return
      if m.is_transparent() :
         m.set_transparency(False)
      if tex_num != -1 :
         glDeleteTextures(self.tex_num)
         self.tex_num = -1
      if not self.is_transparent() :
         self.set_transparency(True)
      if self.bpp != 32 :
         return
      i = 0
      r, g, b = 0, 0, 0
      for tup in m.data :
         r, g, b, a = tup
         self.data[i][3] = int((r + g + b) / 3.0)
