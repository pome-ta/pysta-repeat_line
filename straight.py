from math import radians, sin, cos
from colorsys import hsv_to_rgb
import io
from PIL import Image, ImageFilter
import ui


BG_COLOR = .128
TINT_COLOR = .872
SET_FONT = ('Source Code Pro', 16)

class Draw(ui.View):
  def __init__(self, parent):
    parent.add_subview(self)
    # todo: If you want the background color to be the same as the preview
    #self.bg_color = BG_COLOR
    self.flex = 'WH'
  
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
    for i in range(int(360 *self.v_around)+1):
      radius += self.v_radius
      rad = radians(ang)
      xp = centx + (radius *cos(rad))
      yp = centy + (radius *sin(rad))
      if lastx > -999:
        line = self.p_line(xp, yp, lastx, lasty)
        line.line_width = .64
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
  xp = centx + (radius *cos(rad))
  yp = centy + (radius *sin(rad))
  
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

