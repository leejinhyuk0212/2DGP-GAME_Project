# map.py
from pico2d import *

SW, SH = 800, 600
EDGE = 10  # 화면 좌우 마진

class Map1:
    def __init__(self):
        self.image = load_image('map1.png')

        self.scale   = SH / self.image.h
        self.world_w = int(self.image.w * self.scale)

        self.camera_x = 0.0
        self.target = None
        self._prev_screen_x = None

        self.src_w = int(SW / self.scale)
        self.src_h = self.image.h

    def set_target(self, target):
        self.target = target
        self._prev_screen_x = target.x

    def update(self):
        if not self.target:
            return

        cur = self.target.x
        prev = self._prev_screen_x if self._prev_screen_x is not None else cur
        dx = cur - prev
        self._prev_screen_x = cur

        if cur <= EDGE and dx < 0:
            self.camera_x += dx
            if self.camera_x < 0:
                self.camera_x = 0
            else:
                self.target.x = EDGE
                self._prev_screen_x = self.target.x

        elif cur >= SW - EDGE and dx > 0:
            max_cam = max(0, self.world_w - SW)
            self.camera_x += dx
            if self.camera_x > max_cam:
                self.camera_x = max_cam
            else:
                self.target.x = SW - EDGE
                self._prev_screen_x = self.target.x

        max_cam = max(0, self.world_w - SW)
        if self.camera_x < 0: self.camera_x = 0
        if self.camera_x > max_cam: self.camera_x = max_cam

    def draw(self):
        sx = int(self.camera_x / self.scale)
        self.image.clip_draw_to_origin(sx, 0, self.src_w, self.src_h, 0, 0, SW, SH)

    def get_camera_x(self):
        return self.camera_x
