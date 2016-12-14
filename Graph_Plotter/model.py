class Element(object):
  def __init__(self, screen):
    self.left = 0
    self.top = 0
    self.height = 0
    self.width = 0
    self.background_image = None
    self.background_color = (255, 255, 255)
    self.screen = screen


class Window(Element):
  
    
