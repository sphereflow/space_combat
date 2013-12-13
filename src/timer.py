import sdl2 as sdl


class Timer(object) :
   def __init__(self) :
      self.seconds = 0.0
      self.running = False
      self.paused = False
      self.base = 0
      self.act = 0
      self.last_act = 0
      self.frame = 0
      self.frame_accumulator = 0
      self.frame_time_accumulator = 0.0

   def start(self) :
      if self.running :
         return
      self.base = sdl.SDL_GetTicks()
      self.running = True
      self.paused = False
      self.act = self.last_act = self.base

   def stop(self) :
      self.running = False
      self.paused = False
      self.seconds = 0.0
      self.base = self.act = self.last_act = self.pause_time = 0

   def pause(self) :
      if self.running and (not self.paused) :
         self.pause_time = self.act
         self.paused = True

   def unpause(self) :
      if self.running and self.paused :
         self.base += self.act - self.pause_time
         self.paused = True

   def update(self) :
      if not self.running :
         return
      self.last_act = self.act
      self.act = sdl.SDL_GetTicks()
      if self.paused :
         self.last_act = self.act
      self.frame = (self.act - self.last_act) / 1000.0
      if self.running :
         self.frame_accumulator += 1
         self.frame_time_accumulator += self.frame_time()

   def elapsed_ticks(self) :
      if self.running :
         if self.paused :
            return self.pause_time - self.base
         else :
            return self.act - self.base
      else :
         return 0

   def elapsed_time(self) :
      return self.elapsed_ticks() / 1000.0

   def frame_ticks(self) :
      if not self.running :
         return 0
      if self.paused :
         return 0
      return self.act - self.last_act

   def frame_time(self) :
      self.frame = self.frame_ticks() / 1000.0
      return self.frame

   def frame_rate(self) :
      r = self.frame_accumulator / self.frame_time_accumulator
      self.frame_accumulator = 0
      self.frame_time_accumulator = 0.0
      return r

instance = Timer()

class SubTimer( Timer ) :
   def __init__(self) :
      super().__init__()
      self.interval = 0
      self.rest = 0

   def start(self) :
      super().start()
      self.base = instance.elapsed_ticks() + instance.base
      self.act = self.last_act = self.base

   def pause(self) :
      super().pause()
      if self.running and (not self.paused) :
         self.pause_time = instance.act

   def unpause(self) :
      self.update()
      super().unpause()

   def update(self) :
      if not self.running :
         return
      self.last_act = self.act
      self.act = instance.act
      if self.paused :
         self.last_act = self.act
      self.frame = (self.act - self.last_act) / 1000.0

   def get_interval(self) :
      return self.interval / 1000.0

   def set_interval(self, seconds) :
      if seconds > 0 :
         self.interval = int(seconds * 1000)

   def get_num_passed_intervals(self) :
      if (self.interval <= 0) or (not self.running) :
         return 0
      et = instance.elapsed_ticks() - self.base + instance.base
      if (et < self.interval) or self.paused :
         return 0
      self.rest = et % self.interval
      self.base += et - self.rest
      return int((et - self.rest) / self.interval)

   def get_rest(self) :
      return self.rest / 1000.0
