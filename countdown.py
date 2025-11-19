from pico2d import *

class CountdownSprite:
    def __init__(self):
        self.image = load_image('countdown.png')

        self.frame_w, self.frame_h = 128, 128
        self.cols = 10
        self.total = 60

        self.x, self.y = 400, 550
        self.scale = 0.75
        self.step_time = 1.0

        self.frame = 0
        self.acc = 0.0
        self.done = False

    def update(self, frame_time):
        if self.done:
            return

        self.acc += frame_time
        if self.acc >= self.step_time:
            self.acc -= self.step_time
            self.frame += 1
            if self.frame >= self.total:
                self.done = True

    def draw(self):
        if self.done:
            return

        col = self.frame % self.cols
        row = self.frame // self.cols
        sx = col * self.frame_w
        sy = (5 - row) * self.frame_h

        dw, dh = int(self.frame_w * self.scale), int(self.frame_h * self.scale)
        self.image.clip_draw(sx, sy, self.frame_w, self.frame_h, self.x, self.y, dw, dh)

    def reset(self):
        self.frame = 0
        self.acc = 0.0
        self.done = False
