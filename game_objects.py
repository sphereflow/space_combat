from billboard import *
from math_3d import *
import file_parser as fp
import img_loader as il
from action_evt_model import *
import render_queue as RenderQueue
import timer as Timer
import sound_loader as sl
import animation_loader as AnimationLoader
import collider as Collider

class GameObject( Billboard ) :
   def __init__(self) :
      super().__init__()
      self.children = []
      self.turn_point = np.array([0.0, 0.0, 0.0, 1.0])
      # destruction animation
      self.dest_anim = None
      self.dest_sound = None
      self.slot_positions = []
      self.containers = []

   def render(self) :
      pos_copy = self.m.r.pos.copy()
      ma = np.identity(4)
      set_matrix_rotation(ma, self.m.r.angle)
      self.m.r.pos -= np.dot(ma, self.turn_point)
      self.m.r.pos[3] = 1.0
      super().render()
      self.m.r.pos = pos_copy
      for i, c in enumerate(self.children) :
         c.m.r.pos = self.get_child_pos(i)
         c.render()

   def get_child_pos(self, i) :
      mbuf = np.identity(4)
      set_matrix_rotation(mbuf, self.m.r.angle)
      sp = np.dot(self.slot_positions[i], mbuf)
      return self.m.r.pos + sp

   def destroy(self) :
      if self.dest_sound :
         self.dest_sound.play()
      if self.dest_anim :
         self.dest_anim.m.r.pos = self.m.r.pos.copy()
         self.dest_anim.st.start()
         self.dest_anim.self_destruct = True
         RenderQueue.enqueue(self.dest_anim)
      RenderQueue.dequeue(self)
      UpdateEvent.remove_action(self)
      for container in self.containers :
         if self in container :
            container.remove(self)
      for c in self.children :
         c.destroy()

   def collision_with(self, go) :
      pass
      
  
class Ship( GameObject ) :
   COL_ID = 0
   def __init__(self) :
      super().__init__()
      self.num_slots = 0
      self.hp = 0

   def point_weapons_at(self, v) :
   # for each child construct a line
      for i, c in enumerate(self.children) :
         mbuf = np.identity(4)
         set_matrix_rotation(mbuf, self.m.r.angle)
         sp = np.dot(self.slot_positions[i], mbuf)
         sp[3] = 0.0
         sp = v - (self.m.r.pos + sp)
         sp[3] = 0.0
         sp = sp / npla.norm(sp)
         c.m.r.angle.val = math.acos(np.dot(np.array([0.0, 1.0, 0.0, 0.0]), sp))
         if sp[0] < 0 :
             c.m.r.angle.val *= -1.0
      # TODO : clip to min / max angle
   def collision_with(self, go) :
      if self.hp < 1 :
         self.destroy()

class Weapon( GameObject ) :
   COL_ID = 2
   def __init__(self) :
      super().__init__()
      self.shot = Shot()
      self.shot_timer = Timer.SubTimer()
      self.shot_timer.start()

   def perform(self) :
      # if reload_time has not passed return
      if self.shot_timer.get_num_passed_intervals() < 1 :
          return
      s = self.shot.copy()
      # set a starting position
      s.m.r.pos = self.m.r.pos.copy()
      s.initial_position = self.m.r.pos.copy()
      # set angle
      s.m.r.angle = self.m.r.angle.copy()
      # enqueue in movement
      UpdateEvent.add_action(s.m.fwd)
      # put shot into collider
      Collider.add(s)
      # auto destruction
      UpdateEvent.add_action(s)
      # enqueue in render queue
      RenderQueue.enqueue(s)
      # play a sound
      self.sound.play()

class Shot( GameObject ) :
   COL_ID = 1
   def __init__(self) :
      super().__init__()
      self.travel_distance = 1.0
      self.initial_position = None
      self.damage = 1

   def copy(self) :
      s = Shot()
      s.damage = self.damage
      s.set_texture(self.tex)
      s.m.fwd.ups = self.m.fwd.ups
      s.m.r.width = self.m.r.width
      s.m.r.height = self.m.r.height
      s.travel_distance = self.travel_distance
      s.dest_anim = self.dest_anim.copy()
      s.dest_anim.self_destruct = True
      s.dest_anim.st.start()
      return s

   def perform(self) :
      dist_squared = (self.m.r.pos[0] - self.initial_position[0]) ** 2 + (self.m.r.pos[1] - self.initial_position[1]) ** 2
      if dist_squared > self.travel_distance ** 2 :
         UpdateEvent.remove_action(self)
         self.destroy()

   def destroy(self) :
       super().destroy()
       UpdateEvent.remove_action(self.m.fwd)

   def collision_with(self, go) :
      go.hp -= self.damage
      self.destroy()

def load_game_object(buf, o) :
   o.m.r.width = fp.read_named_float(buf, "width=")
   o.m.r.height = fp.read_named_float(buf, "height=")
   tex = Texture()
   il.load_image(fp.read_named_string(buf, "tex="), tex)
   o.set_texture(tex)
   sdanim = fp.read_named_string(buf, "dest_anim=") 
   sdsound = fp.read_named_string(buf, "dest_sound=")
   if len(sdanim) != 0 :
      o.dest_anim = AnimationLoader.load(sdanim)
   if len(sdsound) != 0 :
      o.dest_sound = sl.load(sdsound)
    
def load_ship(filename) :
   s = Ship()
   buf = open(filename, 'r').read().replace('\n', '')
   s.num_slots = fp.read_named_int(buf, "num_slots=")
   s.hp = fp.read_named_int(buf, "hp=")
   s.m.fwd.ups = fp.read_named_float(buf, "vf")
   s.m.fwd.add_acceleration(fp.read_named_float(buf, "accf="))
   s.m.bwd.ups = fp.read_named_float(buf, "vb")
   s.m.sll.ups = s.m.slr.ups = fp.read_named_float(buf, "vslide=")
   s.m.tr.ups = s.m.tl.ups = fp.read_named_float(buf, "turn_rate=")
   load_game_object(buf, s)
   for i in range(s.num_slots) :
      wbuf = fp.read_named_string(buf, "slot{0}=".format(i+1), "[")
      s.children.append(load_weapon(fp.read_named_string(wbuf, "weapon=")))
      s.slot_positions.append(np.array([0.0, 0.0, 0.0, 1.0]))
      s.slot_positions[i][0] = fp.read_named_float(wbuf, "position_x")
      s.slot_positions[i][1] = fp.read_named_float(wbuf, "position_y")
      s.m.sub_movements.append(s.children[i].m)
   return s

def load_weapon(filename) :
   w = Weapon()
   buf = open(filename, 'r').read().replace('\n', '')
   w.turn_point[0] = fp.read_named_float(buf, "turn_point_x=")
   w.turn_point[1] = fp.read_named_float(buf, "turn_point_y=")
   w.shot_timer.set_interval(fp.read_named_float(buf, "reload_time="))
   w.shot_timer.start()
   load_game_object(buf, w)
   w.shot = load_shot(fp.read_named_string(buf, "shot=", "'"))
   w.sound = sl.load(fp.read_named_string(buf, "sound="))
   return w

def load_shot(sbuf) :
   s = Shot()
   s.m.fwd.ups = fp.read_named_float(sbuf, "v=")
   s.travel_distance = fp.read_named_float(sbuf, "travel_distance=")
   s.damage = fp.read_named_int(sbuf, "damage=")
   load_game_object(sbuf, s)
   return s
