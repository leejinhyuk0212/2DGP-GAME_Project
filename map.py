from pico2d import *

SW, SH = 800, 600
EDGE_MARGIN = 50

class Map1:
    def __init__(self):
        self.image = load_image('map1.png')
        self.scale   = SH / self.image.h
        self.world_w = int(self.image.w * self.scale)
        self.camera_x = 0.0
        self.target = None

        self.src_w = int(SW / self.scale)
        self.src_h = self.image.h

    def set_target(self, target):
        self.target = target

    def update(self):
        if not self.target:
            return

        screen_x = self.target.x - self.camera_x

        if screen_x < EDGE_MARGIN:
            self.camera_x = self.target.x - EDGE_MARGIN
        elif screen_x > SW - EDGE_MARGIN:
            self.camera_x = self.target.x - (SW - EDGE_MARGIN)


        max_cam = max(0, self.world_w - SW)
        if self.camera_x < 0: self.camera_x = 0
        if self.camera_x > max_cam: self.camera_x = max_cam

        if self.target.x < 0: self.target.x = 0
        if self.target.x > self.world_w: self.target.x = self.world_w

    def draw(self):
        sx = int(self.camera_x / self.scale)
        sy = 0
        self.image.clip_draw_to_origin(sx, sy, self.src_w, self.src_h, 0, 0, SW, SH)

    def get_camera_x(self):
        return self.camera_x
