from pico2d import *

class RoundFightOverlay:
    def __init__(self):
        self.image = load_image('round1_fight.png')  # 1행 2열 시트

        # 시트 설정
        self.frame_w, self.frame_h = 512, 160
        self.cols, self.total = 2, 2  # 0: ROUND 1, 1: FIGHT


        self.x, self.y = 400, 300
        self.scale = 1.0

        # 타이밍 (원하면 숫자만 바꿔도 됨)
        self.round_time = 0.8
        self.fight_time = 0.8

        # 상태
        self.frame = 0
        self.acc = 0.0
        self.visible = True
        self.done = False

    def update(self, dt):
        if not self.visible:
            return

        self.acc += dt
        if self.frame == 0:
            if self.acc >= self.round_time:
                self.acc -= self.round_time
                self.frame = 1
        else:
            if self.acc >= self.fight_time:
                self.visible = False
                self.done = True

    def draw(self):
        if not self.visible:
            return
        col = self.frame
        sx = col * self.frame_w
        sy = 0
        dw, dh = int(self.frame_w * self.scale), int(self.frame_h * self.scale)
        self.image.clip_draw(sx, sy, self.frame_w, self.frame_h, self.x, self.y, dw, dh)

    def reset(self):
        self.frame = 0
        self.acc = 0.0
        self.visible = True
        self.done = False

    def should_freeze(self):
        return self.visible