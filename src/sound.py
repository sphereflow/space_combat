import sdl2.sdlmixer as mix
class Sound :
   def __init__(self) :
      self.channels = []

   def play(self) :
      mix.Mix_PlayChannel(-1, self.sound_chunk, 0)
      pass

   def pause(self) :
      pass

   def unpause(self) :
      pass

   def stop(self) :
      pass

   def set_volume(self, vol) :
      pass
