import file_parser as FileParser
from animation import *
import img_loader as ImgLoader

def load(filename) :
   a = Animation()
   buf = open(filename, 'r').read()
   a.m.r.width = FileParser.read_named_float(buf, "width:", "\"")
   a.m.r.height = FileParser.read_named_float(buf, "height:", "\"")
   tex_name = FileParser.read_named_string(buf, "texture:", "\"")
   tex = Texture()
   ImgLoader.load_image(tex_name, tex)
   a.set_texture(tex)
   sp_name = FileParser.read_named_string(buf, "solid_pixel_map", "\"")
   if len(sp_name) > 0 :
      spm = SolidPixelMap()
      ImgLoader.load(sp_name, spm)
      a.spm = spm
   trans_name = FileParser.read_named_string(buf, "transparency_map:", "\"")
   if len(trans_name) > 0 :
      tmap = TransparencyMap()
      ImgLoader.load(trans_name, tmap)
      a.get_texture.apply_transparency_map(tmap)
   a.num_frames = FileParser.read_named_int(buf, "num_frames:", "\"")
   a.st.set_interval(FileParser.read_named_float(buf, "frame_time:", "\""))
   if FileParser.read_named_int(buf, "looping:", "\"") == 1 :
      a.looping = True
   return a
