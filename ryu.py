from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import game_framework
from state_machine import StateMachine
import time

TIME_PER_ACTION = 0.5
FRAMES_PER_ACTION_IDLE = 3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FRAMES_PER_ACTION_RUN = 6


def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Idle:
    def __init__(self, ryu):
        self.ryu = ryu
        self.idle_quads = [
            (328, 1096, 46, 92),  # 7
            (384, 1096, 63, 90),  # 8
            (456, 1096, 55, 91),  # 9
        ]

    def enter(self, e):
        self.ryu.wait_time = get_time()
        self.ryu.dir = 0
        self.ryu.frame = 0.0

    def exit(self, e):
        pass

    def do(self):
        self.ryu.frame = (self.ryu.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 3  # 0,1,2 순환
        self.ryu.idle_frames = [6, 7, 8]
        if get_time() - self.ryu.wait_time > 3:
            self.ryu.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        idx = int(self.ryu.frame)
        sx, sy, sw, sh = self.idle_quads[idx]

        if self.ryu.face_dir == 1:  # 오른쪽
            self.ryu.image.clip_draw(sx, sy, sw, sh, self.ryu.x, self.ryu.y)
        else:  # 왼쪽
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h',
                                               self.ryu.x, self.ryu.y, sw, sh)

class Run:
    def __init__(self, ryu):
        self.ryu = ryu

        self.run_quads = [
            (8, 1096, 38, 95),
            (56, 1096, 45, 94),
            (112, 1096, 45, 93),
            (168, 1096, 35, 95),
            (216, 1096, 45, 94),
            (272, 1096, 47, 93),
        ]

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.ryu.dir = self.ryu.face_dir = 1
        elif left_down(e) or right_up(e):
            self.ryu.dir = self.ryu.face_dir = -1
        self.ryu.frame = 0.0

    def exit(self, e):
        if space_down(e):
            self.ryu.fire_ball()

    def do(self):
        self.ryu.frame = (self.ryu.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_RUN
        # 이동
        self.ryu.x += self.ryu.dir * 5

    def draw(self):
        idx = int(self.ryu.frame)
        sx, sy, sw, sh = self.run_quads[idx]

        if self.ryu.face_dir == 1:  # 오른쪽
            self.ryu.image.clip_draw(sx, sy, sw, sh, self.ryu.x, self.ryu.y)
        else:  # 왼쪽
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h',
                                               self.ryu.x, self.ryu.y, sw, sh)


class Ryu:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('Ch_Ryu.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {space_down: self.IDLE,  right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN : {space_down: self.RUN, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()