from math import radians, sin, cos
from colorsys import hsv_to_rgb
from itertools import product
from random import random
import io
from PIL import Image, ImageFilter
import ui


BG_COLOR = .128
TINT_COLOR = .872
SET_FONT = ('Source Code Pro', 16)

class Perlin:
  def __init__(self):
    permutation = [151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180]
    self.p = [permutation[i % 256] for i in range(512)]
    self.repeat = -1

  def perlin(self, x, y, z):
    if self.repeat > 0:
      x = x % self.repeat
      y = y % self.repeat
      z = z % self.repeat

    xi = int(x) & 255
    yi = int(y) & 255
    zi = int(z) & 255

    xf = x - int(x)
    yf = y - int(y)
    zf = z - int(z)

    u = self.fade(xf)
    v = self.fade(yf)
    w = self.fade(zf)

    aaa = self.p[self.p[self.p[xi]
               + yi] + zi]
    aba = self.p[self.p[self.p[xi]
               + self.inc(yi)] + zi]
    aab = self.p[self.p[self.p[xi]
               + yi] + self.inc(zi)]
    abb = self.p[self.p[self.p[xi]
               + self.inc(yi)] + self.inc(zi)]
    baa = self.p[self.p[self.p[self.inc(xi)]
               + yi] + zi]
    bba = self.p[self.p[self.p[self.inc(xi)]
               + self.inc(yi)] + zi]
    bab = self.p[self.p[self.p[self.inc(xi)]
               + yi] + self.inc(zi)]
    bbb = self.p[self.p[self.p[self.inc(xi)]
               + self.inc(yi)] + self.inc(zi)]

    x1 = self.lerp(self.grad(aaa, xf, yf, zf),
                   self.grad(baa, xf-1, yf, zf), u)
    x2 = self.lerp(self.grad(aba, xf, yf-1, zf),
                  self.grad(bba, xf-1, yf-1, zf),u)
    y1 = self.lerp(x1, x2, v)
    x1 = self.lerp(self.grad(aab, xf, yf, zf-1),
                   self.grad(bab, xf-1, yf, zf-1), u)
    x2 = self.lerp(self.grad(abb, xf, yf-1, zf-1),
                  self.grad(bbb, xf-1, yf-1, zf-1), u)
    y2 = self.lerp(x1, x2, v)
    return (self.lerp(y1, y2, w)+1)/2

  def inc(self, num):
    num += 1
    if self.repeat > 0:
      num %= self.repeat
    return num

  def grad(self, hash, x, y, z):
    h = int(hash) & 15
    u = x if h < 8 else y
    if h < 4: v = y
    elif h == 12 or h == 14: v = x
    else: v = z
    n1 = u if (h&1) == 0 else -(u)
    n2 = v if (h&2) == 0 else -(v)
    return n1 + n2

  def fade(self, t):
    return t *t *t *(t *(t *6-15)+10)

  def lerp(self, a, b, x):
    return a + x * (b - a)


class Draw(ui.View):
  def __init__(self, parent):
    parent.add_subview(self)
    self.flex = 'WH'
    self.pl = Perlin()

  def p_line(self, x1, y1, x2, y2):
    line = ui.Path()
    line.move_to(x1, y1)
    line.line_to(x2, y2)
    return line

  def set_draw(self, v_around=0.0, v_radius=0.0,
                     v_angle=0.0, count=0):
    self.v_around = v_around
    self.v_radius = v_radius
    self.v_angle = v_angle
    self.count = count

  def hsv2rgb(self, count):
    h = count/360
    rgb = hsv_to_rgb(h,1,1)
    return rgb

  def draw(self):
    self.set_needs_display()
    centx = self.width/2
    centy = self.height/2
    lastx = lasty = -999
    radius = ang = 0
    r, g, b = self.hsv2rgb(self.count)
    ui.set_color((r, g, b, .256))
    rad_noise = random()
    for i in range(int(360 *self.v_around)+1):
      rad_noise += .5
      radius += self.v_radius
      rad = radians(ang)
      noise = self.pl.perlin(random(), rad_noise, rad)
      xp = centx + (radius *noise *cos(rad))
      yp = centy + (radius *noise *sin(rad))
      if lastx > -999:
        line = self.p_line(xp, yp, lastx, lasty)
        #line.line_width = .64
        line.line_width = .872
        line.stroke()
      lastx = xp
      lasty = yp
      ang += self.v_angle


class CodeView(ui.View):
  def __init__(self, parent):
    parent.add_subview(self)
    self.alpha = .64
    self.flex = 'WH'
    self.code = self.set_up()

  def set_up(self):
    code = ui.TextView()
    code.bg_color = (0, 0, 0, 0)
    code.text_color = TINT_COLOR
    code.font = SET_FONT
    code.editable = False
    self.add_subview(code)
    code.size_to_fit()
    return code

  def layout(self):
    x = self.width
    y = self.height
    self.code.width = x
    self.code.height = y/2
    self.code.y = y/2 - self.code.height/2


class Parts(ui.View):
  def __init__(self, parent, p_name, num):
    self.parent = parent
    self.parent.add_subview(self)
    self.p_name = str(p_name)
    self.num = num
    self.flex = 'W'
    self.c_slide = self.set_slider()
    self.v_label = self.set_label(1)
    self.n_label = self.set_label(0)
    self.value = 0.0

  def back_value(self, sender):
    if self.num == 1:
      self.value = sender.value *2.0
    if self.num == 2:
      self.value = sender.value *2.0
    if self.num == 3:
      self.value = int(sender.value *360)
    self.v_label.text = str(self.value)
    self.parent.draw()

  def set_slider(self):
    slider = ui.Slider()
    slider.num = self.num
    slider.action = self.back_value
    self.add_subview(slider)
    return slider

  def set_label(self, v=0):
    label = ui.Label()
    label.text_color = TINT_COLOR
    label.font = SET_FONT
    value = self.c_slide.value
    if self.num == 3:
      value = int(value)
    label.text = str(value) if v else self.p_name
    self.add_subview(label)
    label.size_to_fit()
    return label

  def layout(self):
    y = (self.v_label.height + self.c_slide.height) *1.28
    x = self.width
    self.height = y
    self.c_slide.width = x/1.28
    self.c_slide.x = x/2 - self.c_slide.width/2
    self.c_slide.y = y - self.c_slide.height *1.28
    self.v_label.width = x/1.28
    self.v_label.y = self.v_label.height/2.56
    self.v_label.x = self.c_slide.x
    self.n_label.y = self.n_label.height/2.56
    self.n_label.x = x - self.c_slide.x - self.n_label.width



class View(ui.View):
  def __init__(self):
    self.bg_color = BG_COLOR
    self.tint_color = TINT_COLOR
    save_icon = 'iob:ios7_information_32'
    close_icon = 'iob:ios7_close_32'
    left_icon = 'iob:ios7_minus_32'
    right_icon = 'iob:ios7_plus_32'
    self.save_btn = self.create_btn(save_icon)
    self.close_btn = self.create_btn(close_icon)
    self.left_btn = self.create_btn(left_icon)
    self.right_btn = self.create_btn(right_icon)
    self.left_btn.num = 0
    self.right_btn.num = 1
    self.save_btn.action = self.get_img
    self.close_btn.action = self.close_view
    self.left_btn.action = self.cntl_angle
    self.right_btn.action = self.cntl_angle
    self.main = Draw(self)
    self.code_view = CodeView(self)
    self.around = Parts(self, 'around', 1)
    self.radius = Parts(self, 'radius', 2)
    self.angle = Parts(self, 'angle', 3)
    self.add_subview(self.save_btn)
    self.add_subview(self.close_btn)
    self.add_subview(self.left_btn)
    self.add_subview(self.right_btn)
    self.count = 0

  def draw(self):
    self.set_needs_display()
    self.count = self.count +1 if self.count < 360 else 0
    self.txt = f'''\
for i in
  range(int(360*{self.around.value})+1):

  radius += {self.radius.value}
  rad = radians(ang)
  xp = centx + (radius *noise *cos(rad))
  yp = centy + (radius *noise *sin(rad))

  if lastx > -999:
    line = p_line(xp, yp, lastx, lasty)
    line.stroke()

  lastx = xp
  lasty = yp
  ang += {int(self.angle.value)}'''
    self.code_view.code.text = self.txt
    self.main.set_draw(v_around=self.around.value,
                       v_radius=self.radius.value,
                       v_angle=self.angle.value,
                       count = self.count)
    self.main.draw()

  def layout(self):
    x = self.width
    y = self.height
    self.angle.y = y - self.angle.height*1.6
    self.radius.y = self.angle.y - self.radius.height *1.024
    self.around.y = self.radius.y - self.around.height *1.024

    self.close_btn.x = x/1.28 + self.close_btn.width
    self.save_btn.x = self.close_btn.x - self.save_btn.width *1.6
    self.left_btn.x = self.close_btn.x - x/1.28
    self.right_btn.x = self.left_btn.x + self.right_btn.width *1.6
    self.close_btn.y = self.around.y - self.close_btn.width *1.28
    self.save_btn.y = self.close_btn.y
    self.left_btn.y = self.close_btn.y
    self.right_btn.y = self.close_btn.y

  def create_btn(self, icon):
    btn_icon = ui.Image.named(icon)
    btn = ui.Button(image=btn_icon)
    return btn

  def cntl_angle(self, sender):
    value = int(float(self.angle.v_label.text))
    n = 1 if sender.num else -1
    if n < 0:
      value = 361 if value == 0 else value
    if n > 0:
      value = -1 if value == 360 else value
    value += n
    self.angle.value = value
    self.angle.c_slide.value = value/360
    self.angle.v_label.text = str(value)
    self.draw()

  def get_img(self, sender):
    w_im = self.width
    h_im = self.height
    with ui.ImageContext(w_im,h_im) as ctx:
      self.main.draw_snapshot()
      im=ctx.get_image()
      png = im.to_png()
    with Image.open(io.BytesIO(png)) as pil:
      pil.show()

  def close_view(self, sender):
    self.close()



v = View()
v.present(style='fullscreen',
          hide_title_bar=True,
          orientations='portrait')

