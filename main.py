from OpenGL.GL import *
from OpenGL.GLUT import *
import sdl2 as sdl
import sys
from random import *
from input import *
from input_evt import *
import timer as Timer
from billboard import *
import img_loader as ImgLoader
import render_queue as RenderQueue
import numpy as np
import animation_loader as AnimationLoader
from animation import *
from action_evt_model import *
from game_objects import *
import sound_loader as SoundLoader
import collider as Collider

class Game :
   def __init__(self) :
      sdl.SDL_Init(sdl.SDL_INIT_VIDEO)
      sdl.SDL_GL_SetAttribute(sdl.SDL_GL_RED_SIZE, 8)
      sdl.SDL_GL_SetAttribute(sdl.SDL_GL_GREEN_SIZE, 8) 
      sdl.SDL_GL_SetAttribute(sdl.SDL_GL_BLUE_SIZE, 8) 
      sdl.SDL_GL_SetAttribute(sdl.SDL_GL_DEPTH_SIZE, 16) 
      sdl.SDL_GL_SetAttribute(sdl.SDL_GL_DOUBLEBUFFER, 1) 
      sdl.SDL_GL_SetSwapInterval(0)
      StateMachine.Kamera.screen_width = 1920
      StateMachine.Kamera.screen_height = 1080
      self.screen = sdl.SDL_CreateWindow(b"Space Combat", sdl.SDL_WINDOWPOS_UNDEFINED, sdl.SDL_WINDOWPOS_UNDEFINED, StateMachine.Kamera.screen_width, StateMachine.Kamera.screen_height, sdl.SDL_WINDOW_FULLSCREEN | sdl.SDL_WINDOW_OPENGL)
      self.context = sdl.SDL_GL_CreateContext(self.screen)
      self.keyb = Keyboard()
      self.mouse = Mouse()
      glutInit(sys.argv)
      glutInitDisplayMode(GLUT_RGB)
      StateMachine.enable_defaults()
      SoundLoader.initialize()
      self.frame_rate = 0.0
      Timer.instance.start()
      StateMachine.Kamera.set_rect(5.0)
      UpdateEvent.add_trigger(self.keyb)
      UpdateEvent.add_trigger(self.mouse)
      Collider.register_group_ids(0, 1)

   def game_loop(self) :
      while True :
         Timer.instance.update()
         UpdateEvent.trigger()
         if self.keyb.key_down(sdl.SDL_SCANCODE_ESCAPE) :
            sdl.SDL_Quit()
            return
         self.bb.m.r.pos[0] = 2.0 * ((self.mouse.abs_x / 1920.0) - 0.5)
         self.bb.m.r.pos[1] = 2.0 * (-(self.mouse.abs_y / 1080.0) + 0.5)
         self.ship.point_weapons_at(self.mouse.world_position())
         for b in self.bba :
            self.rand_movement(b)
            if self.ship.m.r.contains_vertex_of(b.m.r) or b.m.r.contains_vertex_of(self.ship.m.r) :
               self.rand_vector(b, 5.0)
         if Timer.instance.frame_accumulator == 10 :
            self.frame_rate = Timer.instance.frame_rate()
         Collider.update()
         StateMachine.update_kamera()
         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
         RenderQueue.render()
         StateMachine.enable_texturing(False)
         glLoadIdentity()
         glColor(0xFF, 0xFF, 0xFF)
         glMatrixMode(GL_PROJECTION)
         glLoadIdentity()
         self.glut_print(-0.99, 0.9, "rq:" + str(len(RenderQueue.rq)) + " " + str(self.mouse.abs_y) + " " + str(self.frame_rate))
         StateMachine.enable_texturing(True)
         sdl.SDL_GL_SwapWindow(self.screen)

   def glut_print(self, x, y, text) :
      glRasterPos2f(x, y)
      for c in text :
         glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

   def test(self) :
      StateMachine.Kamera.forward_position = -4.0
      self.bb = Billboard()
      self.bb2 = Billboard()
      self.bba = []
      self.ship = load_ship("crusader.txt")
      self.tex = Texture()
      self.tex2 = Texture()
      self.aie = []
      input_nums = [sdl.SDL_SCANCODE_UP, sdl.SDL_SCANCODE_DOWN, sdl.SDL_SCANCODE_RIGHT, sdl.SDL_SCANCODE_LEFT, sdl.SDL_SCANCODE_W, sdl.SDL_SCANCODE_S, sdl.SDL_SCANCODE_D, sdl.SDL_SCANCODE_A]
      m = StateMachine.Kamera.mov
      StateMachine.Kamera.follow(self.ship.m)
      UpdateEvent.add_trigger(StateMachine.Kamera)
      movs = [m.fwd, m.bwd, m.tr, m.tl]
      m = self.ship.m
      bbmovs = [m.fwd, m.bwd, m.tr, m.tl]
      movs += bbmovs
      bbmovs += movs
      for i in range(7) :
         self.aie.append(InputEvt())
         self.aie[i].input_nr = input_nums[i]
         ActionEvtModel.add_trigger(self.aie[i])
         self.keyb.register_input_evt(self.aie[i])
         self.aie[i].add_action(bbmovs[i])
      # weapon trigger test
      self.shoot_evt = InputEvt()
      #self.shoot_evt.input_nr = sdl.SDL_SCANCODE_SPACE
      self.shoot_evt.input_nr = 1
      ActionEvtModel.add_trigger(self.shoot_evt)
      self.mouse.register_input_evt(self.shoot_evt)
      self.shoot_evt.add_action(self.ship.children[0])
      self.shoot_evt.add_action(self.ship.children[1])
      self.shoot_evt.add_action(self.ship.children[2])
      ImgLoader.load_image("./crusader.png", self.tex)
      ImgLoader.load_image("./1.png", self.tex2)
      self.bb.set_texture(self.tex)
      self.bb.gen_vbo()
      self.bb2.set_texture(self.tex2)
      for i in range(100) :
         self.bba.append(load_ship("crusader.txt"))
         self.bba[i].containers.append(self.bba)
         #self.bba[i].set_texture(self.tex)
         #self.bba[i].m.r.width = 0.05
         #self.bba[i].m.r.height = 0.05
         self.bba[i].gen_dl()
         #self.bba[i].gen_vbo()
         #self.bba[i].gen_va()
         self.rand_vector(self.bba[i], 5.0)
         Collider.add(self.bba[i])
         RenderQueue.enqueue(self.bba[i])
      self.anim = AnimationLoader.load("bomb_anim.txt")
      self.anim.st.start()
      RenderQueue.enqueue(self.anim)
      RenderQueue.enqueue(self.bb2)
      RenderQueue.enqueue(self.ship)
      RenderQueue.enqueue(self.bb)

   def rand_vector(self, bb, fac = 1.0) :
      bb.m.r.pos[0] = fac * (random() * 2 - 1)
      bb.m.r.pos[1] = fac * (random() * 2 - 1)

   def rand_movement(self, bb) :
      i = randrange(100)
      if i == 1 :
         bb.m.fwd.perform()
      if i == 5 :
         bb.m.tl.perform()
      if i == 7 :
         bb.m.tr.perform()
#      if i == 9 :
         #bb.children[0].perform()
         #bb.children[1].perform()
#         bb.children[2].perform()
g = Game()
g.test()
g.game_loop()
