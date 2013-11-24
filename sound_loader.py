import sdl2 as sdl
import sdl2.sdlmixer as mix
from sound import *
import ctypes

sound_map = {}
def initialize() :
   sdl.SDL_InitSubSystem(sdl.SDL_INIT_AUDIO)
   mix.Mix_OpenAudio(22050, sdl.audio.AUDIO_S16SYS, 2, 1024)
   mix.Mix_AllocateChannels(256)

def load(filename) :
   global sound_map
   if filename in sound_map :
      return sound_map[filename]
   else :
      ret = Sound()
      ret.sound_chunk = mix.Mix_LoadWAV(str.encode(filename))
      if not ret.sound_chunk :
         return None
      sound_map[filename] = ret
      return ret
