from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDLK_k, SDLK_l, SDL_KEYUP, SDLK_DOWN, SDLK_COMMA, SDLK_PERIOD, SDLK_UP, SDLK_SLASH
from sdl2 import SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f, SDLK_g, SDLK_v, SDLK_b

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
TIME_PER_ACTION_ATTACK_L = 0.2
TIME_PER_ACTION_ATTACK_H = 0.7
ACTION_PER_TIME_ATTACK_L = 1.0 / TIME_PER_ACTION_ATTACK_L
ACTION_PER_TIME_ATTACK_H = 1.0 / TIME_PER_ACTION_ATTACK_H
TIME_PER_ACTION_ATTACK_COMMA = 0.5
TIME_PER_ACTION_ATTACK_PERIOD = 0.5
ACTION_PER_TIME_ATTACK_COMMA = 1.0 / TIME_PER_ACTION_ATTACK_COMMA
ACTION_PER_TIME_ATTACK_PERIOD = 1.0 / TIME_PER_ACTION_ATTACK_PERIOD

FRAMES_PER_ACTION_RUN = 3
FRAMES_PER_ACTION_IDLE = 3
FRAMES_PER_ACTION_ATTACK = 3
FRAMES_PER_ACTION_SIT = 2

JUMP_ANIM_DURATION = 0.45

time_out = lambda e: e[0] == 'TIMEOUT'

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key ==SDLK_d

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

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
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_COMMA

def period_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_PERIOD

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def land(e):
    return e[0] == 'LAND'

def hit(e):
    return e[0] == 'HIT'

def end_hit(e):
    return e[0] == 'END_HIT'


class Idle:
    def __init__(self, ken):
        self.ken = ken
        self.idle_stand = (328, 936, 48, 94)

    def enter(self, e):
        self.ken.wait_time = get_time()
        self.ken.dir = 0
        self.ken.frame = 0.0

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        sx, sy, sw, sh = self.idle_stand

        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, self.ken.x, self.ken.y)
        else:
            self.ken.image.clip_composite_draw(
                sx, sy, sw, sh, 0, 'h',
                self.ken.x, self.ken.y, sw, sh
            )


class Run:
    def __init__(self, ken):
        self.ken = ken
        self.run_quads = [
            (8, 936, 38, 95),
            (56, 936, 42, 94),
            (112, 936, 46, 93),
            (168, 936, 35, 95),
            (216, 936, 42, 94),
            (272, 936, 47, 93),
        ]

    def enter(self, e):
        if self.ken.right_down(e):
            self.ken.dir = self.ken.face_dir = 1
        elif self.ken.left_down(e):
            self.ken.dir = self.ken.face_dir = -1
        elif self.ken.right_up(e) or self.ken.left_up(e):
            self.ken.dir = self.ken.face_dir = 0
        self.ken.frame = 0.0

    def exit(self, e):
        if self.ken.space_down(e) and hasattr(self.ken, "fire_ball"):
            self.ken.fire_ball()

    def do(self):
        self.ken.frame = (self.ken.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_RUN
        self.ken.x += self.ken.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        idx = int(self.ken.frame)
        sx, sy, sw, sh = self.run_quads[idx]

        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, self.ken.x, self.ken.y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h',
                                               self.ken.x, self.ken.y, sw, sh)

class Hit:
    def __init__(self, ken):
        self.ken = ken
        self.quad = (8, 128, 63, 91)  # 단순 예: idle 프레임 재사용
        self.duration = 0.25
        self.t = 0.0

    def enter(self, e):
        self.t = 0.0
        self.ken.dir = 0
        if (self.ken.state == 'left'):
            self.ken.x -= 10
        else :
            self.ken.x += 10

    def exit(self, e):
        pass

    def do(self):
        self.t += game_framework.frame_time
        if self.t >= self.duration:
            self.ken.state_machine.handle_state_event(('END_HIT', None))

    def draw(self):
        sx, sy, sw, sh = self.quad
        draw_x = self.ken.x
        draw_y = self.ken.y
        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)


class Ken:
    def __init__(self, player=1):
        self.player = player
        self.x, self.y =0, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.state = 'left'
        self.image = load_image('Ch_Ken.png')
        self._camera = None
        self.max_hp = 100
        self.hp = 100
        self.select = 0

        if self.player == 1:
            self.keymap = {
                'LEFT': SDLK_LEFT, 'RIGHT': SDLK_RIGHT, 'UP': SDLK_UP, 'DOWN': SDLK_DOWN,
                'K': SDLK_k, 'L': SDLK_l, 'COMMA': SDLK_COMMA, 'PERIOD': SDLK_PERIOD,
                'SPACE': SDLK_SPACE
            }
        else:
            self.keymap = {
                'LEFT': SDLK_a, 'RIGHT': SDLK_d, 'UP': SDLK_w, 'DOWN': SDLK_s,
                'K': SDLK_f, 'L': SDLK_g, 'COMMA': SDLK_v, 'PERIOD': SDLK_b,
                'SPACE': SDLK_SPACE
            }

        self.time_out = lambda e: e[0] == 'TIMEOUT'
        self.space_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['SPACE']
        self.right_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['RIGHT']
        self.right_up = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == self.keymap['RIGHT']
        self.left_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['LEFT']
        self.left_up = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == self.keymap['LEFT']
        self.k_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['K']
        self.l_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['L']
        self.end_attack = lambda e: e[0] == 'END_ATTACK'
        self.down_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['DOWN']
        self.down_up = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == self.keymap['DOWN']
        self.comma_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['COMMA']
        self.period_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['PERIOD']
        self.up_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['UP']
        self.land = lambda e: e[0] == 'LAND'
        self.hit = lambda e: e[0] == 'HIT'
        self.end_hit = lambda e: e[0] == 'END_HIT'

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.HIT = Hit(self)

        self.is_attacking = False
        self._hit_targets = set()

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    self.right_down: self.RUN, self.left_down: self.RUN,
                    self.right_up: self.RUN, self.left_up: self.RUN,
                    self.hit: self.HIT,
                },
                self.RUN: {
                    self.right_up: self.IDLE, self.left_up: self.IDLE,
                },
                self.HIT: {
                    self.end_hit: self.IDLE,
                }
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

    def get_bb(self):
        return self.x-30, self.y-30,self.x+30,self.y+30

    def handle_collision(self, group, other):
        if group == 'p1:p2':
            if getattr(other, 'is_attacking', False):
                if not hasattr(other, '_hit_targets'):
                    other._hit_targets = set()
                if self not in other._hit_targets:
                    other._hit_targets.add(self)
                    self.take_damage(5)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        if getattr(self, 'state_machine', None) and getattr(self.state_machine, 'cur_state', None) is not getattr(self,'HIT',None):
            self.state_machine.handle_state_event(('HIT', None))