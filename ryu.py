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

def hit(e):
    return e[0] == 'HIT'

def end_hit(e):
    return e[0] == 'END_HIT'


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
        if self.ryu.right_down(e):
            self.ryu.dir = self.ryu.face_dir = 1
        elif self.ryu.left_down(e):
            self.ryu.dir = self.ryu.face_dir = -1
        elif self.ryu.right_up(e) or self.ryu.left_up(e):
            self.ryu.dir = self.ryu.face_dir = 0
        self.ryu.frame = 0.0

    def exit(self, e):
        if self.ryu.space_down(e) and hasattr(self.ryu, "fire_ball"):
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
            'K_L': [(456, 800, 60, 95),(  8, 696, 95, 90),],
            'K_H': [(392, 696, 42, 100),(320, 696, 61, 100),(104, 696, 89, 100),(264, 696, 49, 100),(200, 696, 56, 100),],
        }
        self.attack_type = None
        self.frame = 0.0
        self.action_per_time = 1.0

    def enter(self, e):
        self.ryu.is_attacking = True
        self.ryu._hit_targets.clear()
        self.ryu.frame = 0.0
        sdl = e[1]
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == self.ryu.keymap.get('K'):
                self.attack_type = 'P_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == self.ryu.keymap.get('L'):
                self.attack_type = 'P_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_H * 0.7
            elif sdl.key == self.ryu.keymap.get('COMMA'):
                self.attack_type = 'K_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == self.ryu.keymap.get('PERIOD'):
                self.attack_type = 'K_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD
    def exit(self, e):
        self.ryu.is_attacking = False

    def do(self):
        self.ryu.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time

        if int(self.ryu.frame) >= len(self.attack_frames[self.attack_type]):
            self.ryu.state_machine.handle_state_event(('END_ATTACK', None))

    def draw(self):
        idx = min(int(self.ryu.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]

        base_w = self.attack_frames[self.attack_type][0][2]
        dx = ((sw - base_w) * 0.5)

        base_h = self.attack_frames[self.attack_type][0][3]
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
            'K_L': [ (8, 625, 84, 70) ],
            'K_H': [ (104, 625, 35, 70), (152, 625, 87, 70) ],
        }
        self.attack_type = None
        self.action_per_time = 1.0
        self.frame = 0.0
        self.STAND_H = 92
        self.SIT_H   = 70

    def enter(self, e):
        self.ryu.is_attacking = True
        self.ryu._hit_targets.clear()
        self.ryu.frame = 0.0
        self.frame = 0.0
        sdl = e[1]
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == self.ryu.keymap.get('K'):
                self.attack_type = 'P_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == self.ryu.keymap.get('L'):
                self.attack_type = 'P_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_H * 0.7
            elif sdl.key == self.ryu.keymap.get('COMMA'):
                self.attack_type = 'K_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == self.ryu.keymap.get('PERIOD'):
                self.attack_type = 'K_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD

    def exit(self, e):
        self.ryu.is_attacking = False

    def do(self):
        self.ryu.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time
        if int(self.ryu.frame) >= len(self.attack_frames[self.attack_type]):
            self.ryu.state_machine.handle_state_event(('END_ATTACK', None))

    def draw(self):
        idx = min(int(self.ryu.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]

        base_w = self.attack_frames[self.attack_type][0][2]

        dx = ((sw - base_w) * 0.5)
        STAND_H = 92
        draw_x = self.ryu.x + dx
        draw_y = (self.ryu.y - STAND_H * 0.5) + sh * 0.5

        if self.ryu.state == 'left':
            self.ryu.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h',
                                               draw_x, draw_y, sw, sh)

class Jump_Attack:
    def __init__(self, ryu):
        self.ryu = ryu
        self.attack_frames = {
            'P_L': [(424, 624, 69, 63)],
            'P_H': [(248, 624, 78, 64), (336, 624, 74, 63)],
            'K_L': [(320, 984, 45, 87),(365, 984, 75, 88)],
            'K_H': [(5, 288, 82, 100),(90, 280, 95, 110), (248, 275, 75, 110),(183, 275, 60, 120)]
        }
        self.attack_type = None
        self.action_per_time = 1.0
        self.frame = 0.0
        self.yv = 0.0
        self.ground_y = 0.0

    def enter(self, e):
        self.ryu.is_attacking = True
        self.ryu._hit_targets.clear()
        self.yv = self.ryu.JUMP.yv
        self.ground_y = self.ryu.JUMP.ground_y
        self.ryu.dir = 0
        self.ryu.frame = 0.0

        sdl = e[1] if e and len(e) > 1 else None
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == self.ryu.keymap.get('K'):
                self.attack_type = 'P_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == self.ryu.keymap.get('L'):
                self.attack_type = 'P_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_H * 0.7
            elif sdl.key == self.ryu.keymap.get('COMMA'):
                self.attack_type = 'K_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == self.ryu.keymap.get('PERIOD'):
                self.attack_type = 'K_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD

    def exit(self, e):
        self.ryu.is_attacking = False

    def do(self):
        self.ryu.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time
        if int(self.ryu.frame) >= len(self.attack_frames[self.attack_type]):
            self.ryu.frame = len(self.attack_frames[self.attack_type]) - 1

        self.yv -= GRAVITY * game_framework.frame_time
        self.ryu.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        if self.ryu.y <= self.ground_y:
            self.ryu.y = self.ground_y
            self.ryu.state_machine.handle_state_event(('LAND', None))

    def draw(self):
        idx = min(int(self.ryu.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]

        base_w = self.attack_frames[self.attack_type][0][2]
        dx = ((sw - base_w) * 0.5) * self.ryu.face_dir

        STAND_H = 92
        draw_x = self.ryu.x + dx
        draw_y = (self.ryu.y - STAND_H * 0.5) + sh * 0.5

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

class Jump_Diag:
    def __init__(self, ryu):
        self.ryu = ryu
        self.jump_quads = [
            (50, 990, 48, 100),
            (100, 990, 45, 70),
        ]
        self.yv = 0.0
        self.vx = 0.0
        self.ground_y = 0.0
        self.frame = 0.0

    def enter(self, e):
        self.ground_y = self.ryu.y
        self.yv = JUMP_SPEED
        dir_sign = self.ryu.dir if self.ryu.dir != 0 else (1 if self.ryu.face_dir == 1 else -1)
        self.vx = dir_sign * RUN_SPEED_PPS
        self.frame = 0.0
        self.ryu.air_yv = self.yv
        self.ryu.air_vx = self.vx
        self.ryu.air_ground_y = self.ground_y

    def exit(self, e):
        pass

    def do(self):
        self.yv -= GRAVITY * game_framework.frame_time
        self.ryu.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
        self.ryu.x += self.vx * game_framework.frame_time

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

class Jump_Diag_Attack:
    """대각 점프 중 공격: 공중에서 애니 진행, 가로/세로 속도 적용, 착지 시 Idle."""
    def __init__(self, ryu):
        self.ryu = ryu
        self.attack_frames = {
            'P_L': [(424, 624, 69, 63)],
            'P_H': [(248, 624, 78, 64), (336, 624, 74, 63)],
            'K_L': [(320, 984, 45, 87), (365, 984, 75, 88)],
            'K_H': [(5, 288, 82, 100), (90, 280, 95, 110),
                    (248, 275, 75, 110), (183, 275, 60, 120)]
        }
        self.attack_type = None
        self.action_per_time = 1.0
        self.frame = 0.0
        self.yv = 0.0
        self.vx = 0.0
        self.ground_y = 0.0

    def enter(self, e):
        self.ryu.is_attacking = True
        self.ryu._hit_targets.clear()

        # Jump_Diag에서 저장해둔 공중 상태가 있으면 재사용
        self.yv = getattr(self.ryu, 'air_yv', JUMP_SPEED)
        self.ground_y = getattr(self.ryu, 'air_ground_y', self.ryu.y)

        # 대각 점프와 같은 가로 속도 부여(방향키로 정해진 진행방향 사용)
        dir_sign = self.ryu.dir if self.ryu.dir != 0 else (1 if self.ryu.face_dir == 1 else -1)
        self.vx = dir_sign * RUN_SPEED_PPS

        self.ryu.dir = 0
        self.ryu.frame = 0.0
        self.frame = 0.0

        # 어떤 공격인지 결정 (+ 속도)
        sdl = e[1] if e and len(e) > 1 else None
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == self.ryu.keymap.get('K'):
                self.attack_type = 'P_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == self.ryu.keymap.get('L'):
                self.attack_type = 'P_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_H * 0.7
            elif sdl.key == self.ryu.keymap.get('COMMA'):
                self.attack_type = 'K_L'
                self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == self.ryu.keymap.get('PERIOD'):
                self.attack_type = 'K_H'
                self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD
        if self.attack_type is None:
            self.attack_type = 'P_L'

    def exit(self, e):
        self.ryu.is_attacking = False

    def do(self):
        # 애니메이션 진행(끝 프레임에서 고정)
        self.ryu.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time
        if int(self.ryu.frame) >= len(self.attack_frames[self.attack_type]):
            self.ryu.frame = len(self.attack_frames[self.attack_type]) - 1

        # 공중 물리: 세로/가로 이동
        self.yv -= GRAVITY * game_framework.frame_time
        self.ryu.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
        self.ryu.x += self.vx * game_framework.frame_time

        # 착지 처리
        if self.ryu.y <= self.ground_y:
            self.ryu.y = self.ground_y
            self.ryu.state_machine.handle_state_event(('LAND', None))

    def draw(self):
        idx = min(int(self.ryu.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]

        # 좌하단(발) 기준 고정: 폭/높이 변화 보정
        base_w = self.attack_frames[self.attack_type][0][2]
        dx = ((sw - base_w) * 0.5) * self.ryu.face_dir

        STAND_H = 92
        draw_x = self.ryu.x + dx
        draw_y = (self.ryu.y - STAND_H * 0.5) + sh * 0.5

        if self.ryu.state == 'left':
            self.ryu.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ryu.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)




class Ryu:
    def __init__(self, player=1):
        self.player = player
        self.x, self.y = 0, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.state = 'left'
        self.image = load_image('Ch_Ryu.png')
        self._camera = None
        self.max_hp = 100
        self.hp = 100
        self.select = 0

        if self.player == 1:
            self.keymap = {
                'LEFT': SDLK_LEFT, 'RIGHT': SDLK_RIGHT, 'UP': SDLK_UP, 'DOWN': SDLK_DOWN,
                'K': SDLK_k, 'L': SDLK_l, 'COMMA': SDLK_COMMA, 'PERIOD': SDLK_PERIOD,
                'SPACE': SDLK_SPACE, 'SLASH': SDLK_SLASH
            }
        else:
            self.keymap = {
                'LEFT': SDLK_a, 'RIGHT': SDLK_d, 'UP': SDLK_w, 'DOWN': SDLK_s,
                'K': SDLK_f, 'L': SDLK_g, 'COMMA': SDLK_v, 'PERIOD': SDLK_b,
                'SPACE': SDLK_SPACE, 'SLASH': SDLK_SLASH
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
        self.ATTACK = Normal_Attack(self)
        self.SIT = Sit(self)
        self.JUMP = Jump(self)
        self.CROUCH_ATTACK = Crouch_Attack(self)
        self.JUMP_ATTACK = Jump_Attack(self)
        self.JUMP_DIAG = Jump_Diag(self)
        self.JUMP_DIAG_ATTACK = Jump_Diag_Attack(self)

        self.is_attacking = False
        self._hit_targets = set()

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    self.right_down: self.RUN, self.left_down: self.RUN,
                    self.right_up: self.RUN, self.left_up: self.RUN,
                    self.k_down: self.ATTACK, self.l_down: self.ATTACK,
                    self.comma_down: self.ATTACK, self.period_down: self.ATTACK,
                    self.down_down: self.SIT, self.up_down: self.JUMP,
                },
                self.RUN: {
                    self.right_up: self.IDLE, self.left_up: self.IDLE,
                    self.k_down: self.ATTACK, self.l_down: self.ATTACK,
                    self.comma_down: self.ATTACK, self.period_down: self.ATTACK,
                    self.up_down: self.JUMP_DIAG,
                },
                self.ATTACK: {self.end_attack: self.IDLE},
                self.SIT: {
                    self.k_down: self.CROUCH_ATTACK, self.l_down: self.CROUCH_ATTACK,
                    self.comma_down: self.CROUCH_ATTACK, self.period_down: self.CROUCH_ATTACK,
                    self.down_up: self.IDLE,
                },
                self.CROUCH_ATTACK: {
                    self.k_down: self.CROUCH_ATTACK, self.l_down: self.CROUCH_ATTACK,
                    self.comma_down: self.CROUCH_ATTACK, self.period_down: self.CROUCH_ATTACK,
                    self.end_attack: self.SIT,
                },
                self.JUMP: {
                    self.k_down: self.JUMP_ATTACK, self.l_down: self.JUMP_ATTACK,
                    self.comma_down: self.JUMP_ATTACK, self.period_down: self.JUMP_ATTACK,
                    self.land: self.IDLE,
                },
                self.JUMP_DIAG: {
                    self.k_down: self.JUMP_DIAG_ATTACK, self.l_down: self.JUMP_DIAG_ATTACK,
                    self.comma_down: self.JUMP_DIAG_ATTACK, self.period_down: self.JUMP_DIAG_ATTACK,
                    self.land: self.IDLE,
                },
                self.JUMP_DIAG_ATTACK: {
                    self.k_down: self.JUMP_DIAG_ATTACK, self.l_down: self.JUMP_DIAG_ATTACK,
                    self.comma_down: self.JUMP_DIAG_ATTACK, self.period_down: self.JUMP_DIAG_ATTACK,
                    self.land: self.IDLE,
                },
                self.JUMP_ATTACK: {
                    self.k_down: self.JUMP_ATTACK, self.l_down: self.JUMP_ATTACK,
                    self.comma_down: self.JUMP_ATTACK, self.period_down: self.JUMP_ATTACK,
                    self.land: self.IDLE,
                },
            }
        )

    def update(self):
        self.state_machine.update()

    def set_camera(self, map_obj):
        self._camera = map_obj

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

        if event.type == SDL_KEYDOWN and event.key == SDLK_SLASH:
            self.take_damage(5)


    def draw(self):
        cam_x = self._camera.get_camera_x() if self._camera else 0
        draw_x = self.x - cam_x
        self.state_machine.draw_at(draw_x, self.y)

    def get_bb(self):
        return self.x-30, self.y-30,self.x+30,self.y+30

    def handle_collision(self, group, other):
        # 상대가 공격 중이면, 상대의 히트셋에 없을 때만 데미지 적용
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
        # StateMachine의 현재 상태 속성명은 `cur_state` 이므로 그걸 사용하도록 수정
        if getattr(self, 'state_machine', None) and getattr(self.state_machine, 'cur_state', None) is not getattr(self,'HIT',None):
            self.state_machine.handle_state_event(('HIT', None))