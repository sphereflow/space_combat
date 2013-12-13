import sdl2
import ctypes
import numpy as np
import state_machine as StateMachine

class InputDevice( object ) :
   def __init__(self) :
      self.vie = []

   def register_input_evt(self, evt) :
      if not evt :
         return
      if evt in self.vie :
         return
      self.vie.append(evt)

   def unregister_input_evt(self, evt) :
      if not evt :
         return
      self.vie.remove(evt)

   def update(self) :
      pass

   # this effectively makes InputDevice an Evt without subclassing
   def trigger(self) :
      self.update()

class Keyboard( InputDevice ) :
   def __init__(self) :
      super().__init__()
      self.keymap = []

   def update(self) :
      sdl2.SDL_PumpEvents()
      self.keymap = sdl2.SDL_GetKeyboardState(None)
      for e in self.vie :
         if self.key_down(e.input_nr) :
            e.trigger()

   def key_down(self, key) :
      if not key in range(256) :
         return
      return self.keymap[key] != 0

class Mouse( InputDevice ) :
   def __init__(self) :
      InputDevice.__init__(self)
      self.abs_x = self.abs_y = self.rel_x = self.rel_y = 0

   def update(self) :
      sdl2.SDL_PumpEvents()
      x = ctypes.c_int()
      y = ctypes.c_int()
      self.mouse_state = sdl2.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
      self.rel_x = x.value - self.abs_x
      self.rel_y = y.value - self.abs_y
      self.abs_x = x.value
      self.abs_y = y.value
      for e in self.vie :
         if self.button_down(e.input_nr) :
            e.trigger()

   def world_position(self) :
      r = np.array([2 * StateMachine.Kamera.mov.r.width * (self.abs_x / StateMachine.Kamera.screen_width - 0.5), 2 * StateMachine.Kamera.mov.r.height * (-self.abs_y / StateMachine.Kamera.screen_height + 0.5), 0.0, 1.0])
      return np.dot(r, StateMachine.Kamera.get_mpos())
      
   def button_down(self, ibtn) :
      return sdl2.SDL_BUTTON(ibtn) & self.mouse_state
