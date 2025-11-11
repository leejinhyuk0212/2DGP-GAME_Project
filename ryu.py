from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_k, SDLK_l

import game_framework
from state_machine import StateMachine

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
TIME_PER_ACTION_ATTACK_L = 0.4     # 약공(빠름)
TIME_PER_ACTION_ATTACK_H = 0.7     # 강공(느림)
ACTION_PER_TIME_ATTACK_L = 1.0 / TIME_PER_ACTION_ATTACK_L
ACTION_PER_TIME_ATTACK_H = 1.0 / TIME_PER_ACTION_ATTACK_H

FRAMES_PER_ACTION_RUN = 3
FRAMES_PER_ACTION_IDLE = 3



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

def k_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k

def l_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_l

def end_attack(e):
    return e[0] == 'END_ATTACK'



class Idle:
    def __init__(self, ryu):
        self.ryu = ryu
        self.idle_stand = (328, 1096, 46, 92)

    def enter(self, e):
        self.ryu.wait_time = get_time()
        self.ryu.dir = 0
        self.ryu.frame = 0.0

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        sx, sy, sw, sh = self.idle_stand

        if self.ryu.face_dir == 1:
            self.ryu.image.clip_draw(sx, sy, sw, sh, self.ryu.x, self.ryu.y)
        else:
            self.ryu.image.clip_composite_draw(
                sx, sy, sw, sh, 0, 'h',
                self.ryu.x, self.ryu.y, sw, sh
            )


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
        self.ryu.x += self.ryu.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        idx = int(self.ryu.frame)
        sx, sy, sw, sh = self.run_quads[idx]

        if self.ryu.state == 'left':
            self.ryu.image.clip_draw(sx, sy, sw, sh, self.ryu.x, self.ryu.y)
        else:  # 왼쪽
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h',
                                               self.ryu.x, self.ryu.y, sw, sh)

class Normal_Attack:
    def __init__(self, ryu):
        self.ryu = ryu
        self.attack_frames = {
            'P_L': [
                (8, 800, 61, 92),
                (80, 800, 75, 92),
            ],
            'P_H': [
                (272, 800, 55, 92),
                (336, 800, 47, 92),
                (168, 800, 95, 89),
            ]
        }
        self.attack_type = None
        self.frame = 0.0
        self.action_per_time = 1.0

    def enter(self, e):
        self.ryu.frame = 0.0
        self.start_time = get_time()
        sdl = e[1]
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == SDLK_k:
                self.attack_type = 'P_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == SDLK_l:
                self.attack_type = 'P_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_H

    def exit(self, e):
        pass

    def do(self):
        self.ryu.frame += FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time

        if int(self.ryu.frame) >= len(self.attack_frames[self.attack_type]):
            self.ryu.state_machine.handle_state_event(('END_ATTACK', None))

    def draw(self):
        idx = min(int(self.ryu.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]

        if self.ryu.face_dir == 1:
            self.ryu.image.clip_draw(sx, sy, sw, sh, self.ryu.x, self.ryu.y)
        else:
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h',
                                               self.ryu.x, self.ryu.y, sw, sh)




class Ryu:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.state = 'left'
        self.image = load_image('Ch_Ryu.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.ATTACK = Normal_Attack(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    right_down: self.RUN, left_down: self.RUN,
                    right_up: self.RUN, left_up: self.RUN,
                    k_down: self.ATTACK,  # 약손 입력 → 공격 상태 전환
                    l_down: self.ATTACK,  # 강손 입력 → 공격 상태 전환
                },
                self.RUN: {
                    right_up: self.IDLE, left_up: self.IDLE
                },
                self.ATTACK: {
                    end_attack: self.IDLE
                }
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()