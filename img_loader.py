from PIL import Image
import texture as Tex

img_hash = {}

def load_image(filename, img) :
   if filename in img_hash:
      i = img_hash[filename]
      img.width, img.height, img.bpp , img.btransparent = i.width, i.height, i.bpp, True
      img.data = i.data
      if (type(img) == Tex.Texture) and (type(i) == Tex.Texture) :
         img.tex_num = i.tex_num
         img.stage = i.stage
         img.ref_count = i.ref_count
         img.spm = i.spm
      img.prepare_image()
      return
   surf = Image.open(filename)
   if surf.mode != 'RGBA' :
      surf.convert("RGBA")
   img.width, img.height = surf.size
   img.data = surf.tobytes()
   img.bpp = 32
   img.btransparent = True
   img.prepare_image()
   img_hash[filename] = img
