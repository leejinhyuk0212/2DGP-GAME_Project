from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_k, SDLK_l, SDL_KEYUP, SDLK_DOWN, SDLK_COMMA, SDLK_PERIOD, SDLK_UP

import game_framework
from state_machine import StateMachine

PIXEL_PER_METER = (10.0/0.3)
JUMP_SPEED = 20.0
GRAVITY = 50.0
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
TIME_PER_ACTION_ATTACK_L = 0.2   # 약공(빠름)
TIME_PER_ACTION_ATTACK_H = 0.7    # 강공(느림)
ACTION_PER_TIME_ATTACK_L = 1.0 / TIME_PER_ACTION_ATTACK_L
ACTION_PER_TIME_ATTACK_H = 1.0 / TIME_PER_ACTION_ATTACK_H
TIME_PER_ACTION_ATTACK_COMMA = 0.5   # 약공(빠름)
TIME_PER_ACTION_ATTACK_PERIOD = 0.5    # 강공(느림)
ACTION_PER_TIME_ATTACK_COMMA = 1.0 / TIME_PER_ACTION_ATTACK_COMMA
ACTION_PER_TIME_ATTACK_PERIOD = 1.0 / TIME_PER_ACTION_ATTACK_PERIOD

FRAMES_PER_ACTION_RUN = 3
FRAMES_PER_ACTION_IDLE = 3
FRAMES_PER_ACTION_ATTACK = 3
FRAMES_PER_ACTION_SIT = 2


JUMP_ANIM_DURATION = 0.45

time_out = lambda e: e[0] == 'TIMEOUT'

def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

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

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def comma_down(e):
    return e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_COMMA

def period_down(e):
    return e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_PERIOD

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def land(e):
    return e[0] == 'LAND'



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

        if self.ryu.state == 'left':
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
            'P_L': [(8,800,61,92),(80,800,75,92)],
            'P_H': [(272,800,55,92),(336,800,47,92),(168,800,95,89)],
            'K_L': [(456, 800, 48, 95),(  8, 696, 89, 90),],
        'K_H': [(392, 696, 42, 100),(320, 696, 61, 100),(104, 696, 89, 100),(264, 696, 49, 100),(200, 696, 56, 100),],
        }
        self.attack_type = None
        self.frame = 0.0
        self.action_per_time = 1.0

    def enter(self, e):
        self.ryu.frame = 0.0
        sdl = e[1]
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == SDLK_k:
                self.attack_type = 'P_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == SDLK_l:
                self.attack_type = 'P_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_H
            elif sdl.key == SDLK_COMMA:
                self.attack_type = 'K_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == SDLK_PERIOD:
                self.attack_type = 'K_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD
    def exit(self, e):
        pass

    def do(self):
        self.ryu.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time

        if int(self.ryu.frame) >= len(self.attack_frames[self.attack_type]):
            self.ryu.state_machine.handle_state_event(('END_ATTACK', None))

    def draw(self):
        idx = min(int(self.ryu.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]

        _, _, base_w, base_h = self.attack_frames[self.attack_type][0]
        dx = (sw - base_w) * 0.5 if self.ryu.state == 'left' else -(sw - base_w) * 0.5
        dy = (sh - base_h) * 0.5

        draw_x = self.ryu.x + dx
        draw_y = self.ryu.y + dy

        if self.ryu.state == 'left':
            self.ryu.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)

class Crouch_Attack:
    def __init__(self, ryu):
        self.ryu = ryu
        self.attack_frames =  {
            'P_L': [ (288, 904, 48, 60),(176, 904, 48, 60),(408, 904, 80, 59),],
            'P_H': [(288, 904, 48, 60), (176, 904, 48, 60), (408, 904, 80, 59), ],
            'K_L': [ (8, 625, 84, 60) ],
            'K_H': [ (104, 625, 35, 60), (152, 625, 87, 55) ],
        }
        self.attack_type = None
        self.action_per_time = 1.0
        self.frame = 0.0
        self.STAND_H = 92
        self.SIT_H   = 70

    def enter(self, e):
        self.ryu.dir = 0
        self.frame = 0.0
        sdl = e[1]
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == SDLK_k:
                self.attack_type = 'P_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == SDLK_l:
                self.attack_type = 'P_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_H
            elif sdl.key == SDLK_COMMA:
                self.attack_type = 'K_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == SDLK_PERIOD:
                self.attack_type = 'K_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD

    def exit(self, e): pass

    def do(self):
        self.ryu.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time
        if int(self.ryu.frame) >= len(self.attack_frames[self.attack_type]):
            self.ryu.state_machine.handle_state_event(('END_ATTACK', None))

    def draw(self):
        i = int(self.ryu.frame) % len(self.attack_frames[self.attack_type])
        sx, sy, sw, sh = self.attack_frames[self.attack_type][i]

        draw_x = self.ryu.x
        draw_y = self.ryu.y - (self.STAND_H - self.SIT_H) * 0.5
        if self.ryu.state == 'left':
            self.ryu.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)

class Sit:
    def __init__(self, ryu):
        self.ryu = ryu
        self.quads = [
            (  8, 904, 45, 70),
            ( 64, 904, 47, 70),
        ]
        self.lock_delay = 0.08
        self.t0 = 0.0

    def enter(self, e):
        self.ryu.dir = 0
        self.t0 = get_time()

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        idx = 0 if (get_time() - self.t0) < self.lock_delay else 1
        sx, sy, sw, sh = self.quads[idx]

        STAND_H = 92
        draw_y = (self.ryu.y - STAND_H * 0.5) + sh * 0.5

        if self.ryu.state == 'left':
            self.ryu.image.clip_draw(sx, sy, sw, sh, self.ryu.x, draw_y)
        else:
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', self.ryu.x, draw_y, sw, sh)


class Jump:
    def __init__(self, ryu):
        self.ryu = ryu
        self.jump_quads = [
            (50, 990, 48, 100),
            (100, 990, 45, 70),
        ]
        self.yv = 0.0
        self.ground_y = 0.0
        self.frame = 0.0

    def enter(self, e):
        self.ground_y = self.ryu.y
        self.yv = JUMP_SPEED
        self.frame = 0.0
        self.ryu.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.yv -= GRAVITY * game_framework.frame_time
        self.ryu.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        self.frame = (self.frame + 2 * game_framework.frame_time) % 2

        if self.ryu.y <= self.ground_y:
            self.ryu.y = self.ground_y
            self.ryu.state_machine.handle_state_event(('LAND', None))

    def draw(self):
        idx = int(self.frame)
        sx, sy, sw, sh = self.jump_quads[idx]

        STAND_H = 92
        head_anchor_y = self.ryu.y + STAND_H * 0.5
        draw_y = head_anchor_y - sh * 0.5

        if self.ryu.state == 'left':
            self.ryu.image.clip_draw(sx, sy, sw, sh, self.ryu.x, draw_y)
        else:
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h',
                                               self.ryu.x, draw_y, sw, sh)


class Ryu:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.state = 'left'
        self.image = load_image('Ch_Ryu.png')
        self._camera = None

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.ATTACK = Normal_Attack(self)
        self.SIT = Sit(self)
        self.JUMP = Jump(self)
        self.CROUCH_ATTACK = Crouch_Attack(self)


        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    right_down: self.RUN, left_down: self.RUN,
                    right_up: self.RUN, left_up: self.RUN,
                    k_down: self.ATTACK,  # 약손 입력 → 공격 상태 전환
                    l_down: self.ATTACK,  # 강손 입력 → 공격 상태 전환
                    comma_down: self.ATTACK,
                    period_down: self.ATTACK,
                    down_down: self.SIT,
                    up_down: self.JUMP,
                },
                self.RUN: {
                    right_up: self.IDLE, left_up: self.IDLE,
                    k_down: self.ATTACK,
                    l_down: self.ATTACK,
                    comma_down: self.ATTACK,
                    period_down: self.ATTACK,
                    up_down: self.JUMP
                },
                self.ATTACK: {
                    end_attack: self.IDLE
                },
                self.SIT: {
                    k_down: self.CROUCH_ATTACK,
                    l_down: self.CROUCH_ATTACK,
                    comma_down: self.CROUCH_ATTACK,
                    period_down: self.CROUCH_ATTACK,
                    down_up: self.IDLE,
                },
                self.CROUCH_ATTACK: {
                    end_attack: self.SIT
                },
                self.JUMP: {
                    land: self.IDLE,  # 착지하면 Idle로
                },
            }
        )

    def update(self):
        self.state_machine.update()

    def set_camera(self, map_obj):
        self._camera = map_obj

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        cam_x = self._camera.get_camera_x() if self._camera else 0
        draw_x = self.x - cam_x
        self.state_machine.draw_at(draw_x, self.y)