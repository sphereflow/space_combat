import action

class Evt( object ) :
   def __init__(self) :
      self.va = []
      self.ve = []

   def trigger(self) :
      for e in self.ve :
         e.trigger()
      for a in self.va :
         a.perform()

   def add_trigger(self, e) :
      self.ve.append(e)

   def remove_trigger(self, e) :
      if e in self.ve :
         self.ve.remove(e)

   def add_action(self, a) :
      self.va.append(a)

   def remove_action(self, a) :
      if a in self.va :
         self.va.remove(a)
