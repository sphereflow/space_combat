from OpenGL import GL, GLU
from kamera import *
from math_3d import *

s_errors = ""

def enable_defaults() :
   global s_errors
   GL.glClearColor(0, 0, 0, 0)
   GL.glDisable(GL.GL_LIGHTING)
   GL.glDisable(GL.GL_CULL_FACE)
   GL.glCullFace(GL.GL_BACK)
   GL.glDepthFunc(GL.GL_LEQUAL)
   enable_alpha_blending(True)
   GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
   GL.glEnableClientState(GL.GL_TEXTURE_COORD_ARRAY)
   enable_texturing(True)
   GL.glShadeModel(GL.GL_FLAT)
   GL.glMatrixMode(GL.GL_MODELVIEW)
   Kamera.set_rect(1)
   check_errors("enable_defaults")

def enable_texturing(b) :
   if b :
      GL.glEnable(GL.GL_TEXTURE_2D)
   else :
      GL.glDisable(GL.GL_TEXTURE_2D)

def enable_alpha_blending(b) :
   if b :
      GL.glEnable(GL.GL_BLEND)
      GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
   else :
      GL.glDisable(GL.GL_BLEND)

def set_texture(t) :
   if t.tex_num == -1 :
      t.prepare_image()
   GL.glBindTexture(GL.GL_TEXTURE_2D, t.tex_num)
   GL.glActiveTexture(GL.GL_TEXTURE0 + t.get_stage)

def set_model_view(mv) :
   GL.glLoadMatrixf(mv)

def update_kamera() :
   mbuf = Kamera.get_mpos()
   mbuf = npla.inv(mbuf)
   mbuf = np.dot(mbuf, Kamera.projection)
   GL.glMatrixMode(GL.GL_PROJECTION)
   GL.glLoadMatrixf(mbuf)
   GL.glMatrixMode(GL.GL_MODELVIEW)

def set_viewport(x, y, w, h) :
   GL.glViewport(x, y, w, h)

def check_errors(source) :
   global s_errors
   s_errors += source + "\n" + str(GLU.gluErrorString(GL.glGetError())) + "\n\n"

def output_matrices() :
   global s_errors
   s_errors += "Modelview Matrix :\n"
   s_errors += str(GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)) + "\n"
   s_errors += "Projection Matrix :\n"
   s_errors += str(GL.glGetFloatv(GL.GL_PROJECTION_MATRIX)) + "\n"
