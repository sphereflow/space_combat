from image import *

class SolidPixelMap( Image ) :
   def __init__(self) :
      pass

   def prepare_image(self) :
      if bpp == 32 :
         self.set_transparency(False)
      if not data :
         return
      mask = 0x01
      npixels = self.width * self.height
      spm_size = int(npixels / 8)
      if (npixels % 8) != 0 :
         spm_size += 1
      spm = []
      bit_index = byte_index = 0
      for index in range(npixels) :
         if bit_index == 8 :
            bit_index = 0
            mask = 0x01
            byte_index += 1
            spm[byte_index] = 0x00
         else :
            mask <<= 1
            bit_index += 1
         r, g, b = self.data[index]
         if ((r + g + b) / 3.0) > 127 :
            spm[byte_index] |= mask
         self.data = spm
         self.bpp = 1

      def edge_only(self) :
         npixels = self.width * self.height
         spm_size = int(npixels / 8)
         if (npixels % 8) != 0 :
            spm_size += 1
         spm_edge = []
         for i in range(npixels) :
            spm_edge[i] = 0x00
         # _l stands for local
         bit_index = byte_index = bi_l = by_l = 0
         mask = m_l = 0x00
         for y in range(self.height) :
            for x in range(self.width) :
               bit_index = y * self.width + x
               mask = 0x01 << (bit_index % 8)
               if (self.data[byte_index] & mask) != 0x00 :
                  for y_l in range(-1, 2) :
                     for x_l in range(-1, 2) :
                        bi_l = (y + y_l) * self.width + x + x_l
                        by_l = int(bi_l / 8)
                        m_l = 0x01 << (bi_l % 8)
                        if (data[by_l] % m_l) == 0x00 :
                           spm_edge[byte_index] |= mask
                           continue
         self.data = spm_edge

      def is_solid(self, x, y) :
         if (not x in range(width)) or (not y in range(height)) :
            return False
         index = x + self.width * y
         bit_index = index % 8
         byte_index = int(index / 8)
         return (data[byte_index] & (0x01 << bit_index)) != 0x00
