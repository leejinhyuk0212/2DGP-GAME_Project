from pico2d import *

class HealthBar:
    def __init__(self, player):
        self.player = player
        self.x = 0
        self.y = 0
        self.width=300
        self.height=22
        self.image = load_image('hp_bar.png')
        self.hp = player.hp


    def update(self):
        self.hp = self.player.hp

    def draw(self):
        if (self.player.state == 'left'):
            hp_w = self.hp * 3
            left_x = 170 - (self.width - hp_w) / 2
            self.image.clip_draw(0, 0, hp_w, self.height, left_x, 550)
        else:
            hp_w = self.hp * 3
            right_x = 630 + (self.width - hp_w) / 2
            self.image.clip_draw(0, 0, hp_w, self.height, right_x, 550)
