from pico2d import *

class HealthBar:
    def __init__(self, ryu):
        self.ryu = ryu
        self.x = 0
        self.y = 0
        self.width=300
        self.height=22
        self.image = load_image('hp_bar.png')

    def update(self):
        pass

    def draw(self):

        self.image.clip_draw(self.x, self.y ,self.width, self.height, 170, 550)