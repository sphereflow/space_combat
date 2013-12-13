class Image( object ) :
   def __init__(self) :
      self.width = self.height = 0
      self.btransparent = False
      self.bpp = 24

   def is_transparent(self) :
      return self.btransparent

   def set_transparency(self, btrans) :
      if btrans == self.btransparent :
         return
      self.btransparent = btrans
      if self.btransparent :
         self.bpp = 32
         if self.data :
            for i in range(self.width * self.height + 1) :
               self.data.insert(i * 4 + 3, 0)
      else :
         self.bpp = 24
         if self.data :
            self.data.delete_at(i * 3 + 3)

   def prepare_image(self) :
      pass
