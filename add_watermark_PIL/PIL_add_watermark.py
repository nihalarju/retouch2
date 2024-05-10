
# import all the libraries
from PIL import Image
from PIL import ImageFont, ImageDraw, ImageOps
import os
import random
import glob

# fname = "/Users/narju/Documents/code/educative/retouch/add_watermark_PIL/obj2__0.png"
sourcedir = "/Users/narju/Documents/code/data/coil-100/" 
targetdir = "/Users/narju/Documents/code/educative/retouch/watermarked/"
# fname = "obj2__0.png"

texts = ["Nihal Arju", "nihal.arju@intel.com"]

# add watermark to 'image_file': str at 'angle':int with 'text': list
def add_watermark(im, texts, angle = 45):
  # image opening
  w, h = im.size
  font_size = w//8 if h > w else h//8 
  font_size = random.randint(font_size*0.5, font_size*1.5)
  wim = im.copy().rotate(-angle, expand=True).convert("RGBA") #watermark image
  fnt = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", int(font_size/2))

  txt_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(50,200))

  txt = Image.new("RGBA", wim.size, (255, 255, 255, 0))
  d = ImageDraw.Draw(txt)
  text_w, text_h = random.randint(w*.25, w*.75), random.randint(h*.25, h*.75)
  for text in texts:
    d.text((text_w, text_h) , text, font=fnt, fill=txt_color)
    text_h += font_size//2
  out = Image.alpha_composite(wim, txt)
  out = out.rotate(angle, expand = True)
  wp, hp = out.size
  sw, sh = (wp-w)//2, (hp-h)//2
  out = out.crop(box = (sw, sh, w+sw, h+sh))
  # print(full_path)
  # out.save(output_image_path)
  return out


fnames = glob.glob(sourcedir + "*.png")
for fname in fnames:
  # print(fname)
  input_image_path = os.path.join(sourcedir, os.path.basename(fname))
  angle = random.randint(15,80)
  im = Image.open(input_image_path)
  out = add_watermark(im, angle=angle, texts=texts)
  out = out.convert("RGB")
  output_image_path = os.path.join(targetdir, os.path.basename(fname))
  out.save(output_image_path)

print("done! ")