from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDLK_k, SDLK_l, SDL_KEYUP, SDLK_DOWN, SDLK_COMMA, SDLK_PERIOD, SDLK_UP, SDLK_SLASH
from sdl2 import SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f, SDLK_g, SDLK_v, SDLK_b, SDLK_c

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

def dead(e):
    return e[0] == 'DEAD'


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

class Normal_Attack:
    def __init__(self, ken):
        self.ken = ken
        # 플레이스홀더: 실제 좌표로 교체하세요
        self.attack_frames = {
            'P_L': [ (8, 640, 61, 92), (80, 640, 74, 92) ],
            'P_H': [ (272, 640, 54, 92), (336, 640, 47, 92), (168, 640, 93, 89) ],
            'K_L': [ (456,640,48,93), (8,536,89,84) ],
            'K_H': [ (392, 536, 37, 90), (320, 536, 59, 88), (100, 536, 87, 83),
                     (264,536,47,93),(200,536,53,95)],
        }
        self.attack_type = None
        self.frame = 0.0
        self.action_per_time = 1.0

    def enter(self, e):
        self.ken.is_attacking = True
        self.ken._hit_targets.clear()
        self.ken.frame = 0.0
        sdl = e[1] if e and len(e) > 1 else None
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == self.ken.keymap.get('K'):
                self.attack_type = 'P_L'; self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == self.ken.keymap.get('L'):
                self.attack_type = 'P_H'; self.action_per_time = ACTION_PER_TIME_ATTACK_H * 0.7
            elif sdl.key == self.ken.keymap.get('COMMA'):
                self.attack_type = 'K_L'; self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == self.ken.keymap.get('PERIOD'):
                self.attack_type = 'K_H'; self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD

    def exit(self, e):
        self.ken.is_attacking = False

    def do(self):
        self.ken.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time
        if int(self.ken.frame) >= len(self.attack_frames[self.attack_type]):
            self.ken.state_machine.handle_state_event(('END_ATTACK', None))

    def draw(self):
        idx = min(int(self.ken.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]

        base_w = self.attack_frames[self.attack_type][0][2]
        dx = ((sw - base_w) * 0.5) * self.ken.face_dir

        base_h = self.attack_frames[self.attack_type][0][3]
        dy = (sh - base_h) * 0.5

        draw_x = self.ken.x + dx
        draw_y = self.ken.y + dy

        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)

class Crouch_Attack:
    def __init__(self, ken):
        self.ken = ken
        # 플레이스홀더: 실제 좌표로 교체하세요
        self.attack_frames = {
            'P_L': [ (288,744,48,60), (176,744,48,60),(408,744,79,59) ],
            'P_H': [ (288,744,48,60), (176,744,48,60),(408,744,79,59) ],
            'K_L': [ (208, 464, 85, 61) ],
            'K_H': [ (304, 464, 36, 31),(136,464,64,59), (352, 464, 88, 56) ],
        }
        self.attack_type = None
        self.action_per_time = 1.0
        self.frame = 0.0
        self.STAND_H = 92
        self.SIT_H = 70

    def enter(self, e):
        self.ken.is_attacking = True
        self.ken._hit_targets.clear()
        self.ken.frame = 0.0
        sdl = e[1] if e and len(e) > 1 else None
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == self.ken.keymap.get('K'):
                self.attack_type = 'P_L'; self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == self.ken.keymap.get('L'):
                self.attack_type = 'P_H'; self.action_per_time = ACTION_PER_TIME_ATTACK_H * 0.7
            elif sdl.key == self.ken.keymap.get('COMMA'):
                self.attack_type = 'K_L'; self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == self.ken.keymap.get('PERIOD'):
                self.attack_type = 'K_H'; self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD

    def exit(self, e):
        self.ken.is_attacking = False

    def do(self):
        self.ken.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time
        if int(self.ken.frame) >= len(self.attack_frames[self.attack_type]):
            self.ken.state_machine.handle_state_event(('END_ATTACK', None))

    def draw(self):
        idx = min(int(self.ken.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]
        base_w = self.attack_frames[self.attack_type][0][2]
        dx = ((sw - base_w) * 0.5) * self.ken.face_dir
        STAND_H = 92
        draw_x = self.ken.x + dx
        draw_y = (self.ken.y - STAND_H * 0.5) + sh * 0.5
        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)

class Jump:
    def __init__(self, ken):
        self.ken = ken
        # 플레이스홀더
        self.jump_quads = [ (128,833,31,94), (72,833,45,86) ]
        self.yv = 0.0
        self.ground_y = 0.0
        self.frame = 0.0

    def enter(self, e):
        self.ground_y = self.ken.y
        self.yv = JUMP_SPEED
        self.frame = 0.0
        self.ken.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.yv -= GRAVITY * game_framework.frame_time
        self.ken.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
        self.frame = (self.frame + 2 * game_framework.frame_time) % 2
        if self.ken.y <= self.ground_y:
            self.ken.y = self.ground_y
            self.ken.state_machine.handle_state_event(('LAND', None))

    def draw(self):
        idx = int(self.frame)
        sx, sy, sw, sh = self.jump_quads[idx]
        STAND_H = 92
        head_anchor_y = self.ken.y + STAND_H * 0.5
        draw_y = head_anchor_y - sh * 0.5
        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, self.ken.x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', self.ken.x, draw_y, sw, sh)

class Jump_Attack:
    def __init__(self, ken):
        self.ken = ken
        # 플레이스홀더
        self.attack_frames = {
            'P_L': [ (184, 360, 69, 61) ],
            'P_H': [ (96, 360, 74, 64) ],
            'K_L': [ (488,832,46,64),(544,832,75,88) ],
            'K_H': [ (184, 232, 77, 79), (272, 232, 86, 80), (432,232, 64, 88), (368, 232, 55, 88) ],
        }
        self.attack_type = None
        self.action_per_time = 1.0
        self.frame = 0.0
        self.yv = 0.0
        self.ground_y = 0.0

    def enter(self, e):
        self.ken.is_attacking = True
        self.ken._hit_targets.clear()
        # 현재 점프 상태에서 정보 가져오기
        self.yv = getattr(self.ken.JUMP, 'yv', JUMP_SPEED)
        self.ground_y = getattr(self.ken.JUMP, 'ground_y', self.ken.y)
        self.ken.dir = 0
        self.ken.frame = 0.0
        sdl = e[1] if e and len(e) > 1 else None
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == self.ken.keymap.get('K'):
                self.attack_type = 'P_L'; self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == self.ken.keymap.get('L'):
                self.attack_type = 'P_H'; self.action_per_time = ACTION_PER_TIME_ATTACK_H * 0.7
            elif sdl.key == self.ken.keymap.get('COMMA'):
                self.attack_type = 'K_L'; self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == self.ken.keymap.get('PERIOD'):
                self.attack_type = 'K_H'; self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD

    def exit(self, e):
        self.ken.is_attacking = False

    def do(self):
        self.ken.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time
        if int(self.ken.frame) >= len(self.attack_frames[self.attack_type]):
            self.ken.frame = len(self.attack_frames[self.attack_type]) - 1
        # 공중 물리
        self.yv -= GRAVITY * game_framework.frame_time
        self.ken.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
        if self.ken.y <= self.ground_y:
            self.ken.y = self.ground_y
            self.ken.state_machine.handle_state_event(('LAND', None))


    def draw(self):
        idx = min(int(self.ken.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]
        base_w = self.attack_frames[self.attack_type][0][2]
        dx = ((sw - base_w) * 0.5) * self.ken.face_dir
        STAND_H = 92
        draw_x = self.ken.x + dx
        draw_y = (self.ken.y - STAND_H * 0.5) + sh * 0.5
        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)

class Jump_Diag:
    def __init__(self, ken):
        self.ken = ken
        self.jump_quads = [ (128,833,31,94), (72,833,45,86)  ]  # 플레이스홀더
        self.yv = 0.0
        self.vx = 0.0
        self.ground_y = 0.0
        self.frame = 0.0

    def enter(self, e):
        self.ground_y = self.ken.y
        self.yv = JUMP_SPEED
        dir_sign = self.ken.dir if self.ken.dir != 0 else (1 if self.ken.face_dir == 1 else -1)
        self.vx = dir_sign * RUN_SPEED_PPS
        self.frame = 0.0
        self.ken.air_yv = self.yv
        self.ken.air_vx = self.vx
        self.ken.air_ground_y = self.ground_y

    def exit(self, e):
        pass

    def do(self):
        self.yv -= GRAVITY * game_framework.frame_time
        self.ken.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
        self.ken.x += self.vx * game_framework.frame_time
        self.frame = (self.frame + 2 * game_framework.frame_time) % 2
        if self.ken.y <= self.ground_y:
            self.ken.y = self.ground_y
            self.ken.state_machine.handle_state_event(('LAND', None))

    def draw(self):
        idx = int(self.frame)
        sx, sy, sw, sh = self.jump_quads[idx]
        STAND_H = 92
        head_anchor_y = self.ken.y + STAND_H * 0.5
        draw_y = head_anchor_y - sh * 0.5
        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, self.ken.x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', self.ken.x, draw_y, sw, sh)

class Jump_Diag_Attack:
    def __init__(self, ken):
        self.ken = ken
        # 플레이스홀더
        self.attack_frames = {
            'P_L': [(184, 360, 69, 61)],
            'P_H': [(96, 360, 74, 64)],
            'K_L': [(488, 832, 46, 64), (544, 832, 75, 88)],
            'K_H': [(184, 232, 77, 79), (272, 232, 86, 80), (432, 232, 64, 88), (368, 232, 55, 88)],
        }
        self.attack_type = None
        self.action_per_time = 1.0
        self.frame = 0.0
        self.yv = 0.0
        self.vx = 0.0
        self.ground_y = 0.0

    def enter(self, e):
        self.ken.is_attacking = True
        self.ken._hit_targets.clear()
        self.yv = getattr(self.ken, 'air_yv', JUMP_SPEED)
        self.ground_y = getattr(self.ken, 'air_ground_y', self.ken.y)
        dir_sign = self.ken.dir if self.ken.dir != 0 else (1 if self.ken.face_dir == 1 else -1)
        self.vx = dir_sign * RUN_SPEED_PPS
        self.ken.dir = 0
        self.ken.frame = 0.0
        sdl = e[1] if e and len(e) > 1 else None
        if sdl and sdl.type == SDL_KEYDOWN:
            if sdl.key == self.ken.keymap.get('K'):
                self.attack_type = 'P_L'; self.action_per_time = ACTION_PER_TIME_ATTACK_L
            elif sdl.key == self.ken.keymap.get('L'):
                self.attack_type = 'P_H'; self.action_per_time = ACTION_PER_TIME_ATTACK_H * 0.7
            elif sdl.key == self.ken.keymap.get('COMMA'):
                self.attack_type = 'K_L'; self.action_per_time = ACTION_PER_TIME_ATTACK_COMMA
            elif sdl.key == self.ken.keymap.get('PERIOD'):
                self.attack_type = 'K_H'; self.action_per_time = ACTION_PER_TIME_ATTACK_PERIOD
        if self.attack_type is None:
            self.attack_type = 'P_L'

    def exit(self, e):
        self.ken.is_attacking = False

    def do(self):
        self.ken.frame += FRAMES_PER_ACTION_ATTACK * self.action_per_time * game_framework.frame_time
        if int(self.ken.frame) >= len(self.attack_frames[self.attack_type]):
            self.ken.frame = len(self.attack_frames[self.attack_type]) - 1
        self.yv -= GRAVITY * game_framework.frame_time
        self.ken.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
        self.ken.x += self.vx * game_framework.frame_time
        if self.ken.y <= self.ground_y:
            self.ken.y = self.ground_y
            self.ken.state_machine.handle_state_event(('LAND', None))

    def draw(self):
        idx = min(int(self.ken.frame), len(self.attack_frames[self.attack_type]) - 1)
        sx, sy, sw, sh = self.attack_frames[self.attack_type][idx]
        base_w = self.attack_frames[self.attack_type][0][2]
        dx = ((sw - base_w) * 0.5) * self.ken.face_dir
        STAND_H = 92
        draw_x = self.ken.x + dx
        draw_y = (self.ken.y - STAND_H * 0.5) + sh * 0.5
        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)

class Sit:
    def __init__(self, ken):
        self.ken = ken
        # 플레이스홀더
        self.quads = [ (8,744,45,80), (64,744,47,63) ]
        self.lock_delay = 0.08
        self.t0 = 0.0

    def enter(self, e):
        self.ken.dir = 0
        self.t0 = get_time()

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        idx = 0 if (get_time() - self.t0) < self.lock_delay else 1
        sx, sy, sw, sh = self.quads[idx]
        STAND_H = 92
        draw_y = (self.ken.y - STAND_H * 0.5) + sh * 0.5
        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, self.ken.x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', self.ken.x, draw_y, sw, sh)

class Dead:
    def __init__(self, ken):
        self.ken = ken
        self.quads = [(200, 128, 63, 62), (272, 128, 103, 31)]
        self.duration = 2.0
        self.t = 0.0

    def enter(self, e):
        self.t = 0.0
        self.ken.dir = 0
        self.ken.frame = 0.0

    def exit(self, e):
        pass

    def do(self):
        self.t += game_framework.frame_time
        if self.t >= self.duration:
            game_framework.quit()

    def draw(self):
        frame_count = len(self.quads)
        idx = min(int((self.t / self.duration) * frame_count), frame_count - 1)
        sx, sy, sw, sh = self.quads[idx]
        STAND_H = 92
        draw_y = (self.ken.y - STAND_H * 0.5) + sh * 0.5
        draw_x = self.ken.x
        if self.ken.state == 'left':
            self.ken.image.clip_draw(sx, sy, sw, sh, draw_x, draw_y)
        else:
            self.ken.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', draw_x, draw_y, sw, sh)

class Guard:
    def __init__(self, fighter):
        self.fighter = fighter
        self.quad = (392, 640, 56, 92)

    def enter(self, e):
        self.fighter.is_guarding = True
        self.fighter.dir = 0
        self.fighter.frame = 0.0

    def exit(self, e):
        self.fighter.is_guarding = False

    def do(self):
        pass

    def draw(self):
        sx, sy, sw, sh = self.quad
        STAND_H = 92
        draw_y = (self.fighter.y - STAND_H * 0.5) + sh * 0.5
        if self.fighter.state == 'left':
            self.fighter.image.clip_draw(sx, sy, sw, sh, self.fighter.x, draw_y)
        else:
            self.fighter.image.clip_composite_draw(sx, sy, sw, sh, 0, 'h', self.fighter.x, draw_y, sw, sh)


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
                'SPACE': SDLK_SPACE, 'SLASH': SDLK_SLASH, 'BLOCK': SDLK_SLASH
            }
        else:
            self.keymap = {
                'LEFT': SDLK_a, 'RIGHT': SDLK_d, 'UP': SDLK_w, 'DOWN': SDLK_s,
                'K': SDLK_f, 'L': SDLK_g, 'COMMA': SDLK_v, 'PERIOD': SDLK_b,
                'SPACE': SDLK_SPACE, 'SLASH': SDLK_SLASH, 'BLOCK': SDLK_c
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
        self.dead = lambda e: e[0] == 'DEAD'
        self.block_down = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == self.keymap['BLOCK']
        self.block_up = lambda e: e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == self.keymap['BLOCK']

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.ATTACK = Normal_Attack(self)
        self.SIT = Sit(self)
        self.JUMP = Jump(self)
        self.CROUCH_ATTACK = Crouch_Attack(self)
        self.JUMP_ATTACK = Jump_Attack(self)
        self.JUMP_DIAG = Jump_Diag(self)
        self.JUMP_DIAG_ATTACK = Jump_Diag_Attack(self)
        self.HIT = Hit(self)
        self.DEAD = Dead(self)
        self.GUARD = Guard(self)

        self.is_guarding = False
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
                    self.hit: self.HIT, self.dead: self.DEAD,
                    self.block_down: self.GUARD,
                },
                self.RUN: {
                    self.right_up: self.IDLE, self.left_up: self.IDLE,
                    self.k_down: self.ATTACK, self.l_down: self.ATTACK,
                    self.comma_down: self.ATTACK, self.period_down: self.ATTACK,
                    self.up_down: self.JUMP_DIAG, self.hit: self.HIT, self.dead: self.DEAD,
                    self.block_down: self.GUARD,
                },
                self.ATTACK: {self.end_attack: self.IDLE},
                self.SIT: {
                    self.k_down: self.CROUCH_ATTACK, self.l_down: self.CROUCH_ATTACK,
                    self.comma_down: self.CROUCH_ATTACK, self.period_down: self.CROUCH_ATTACK,
                    self.down_up: self.IDLE, self.hit: self.HIT, self.dead: self.DEAD,
                    self.block_down: self.GUARD,
                },
                self.CROUCH_ATTACK: {
                    self.k_down: self.CROUCH_ATTACK, self.l_down: self.CROUCH_ATTACK,
                    self.comma_down: self.CROUCH_ATTACK, self.period_down: self.CROUCH_ATTACK,
                    self.end_attack: self.SIT, self.hit: self.HIT, self.dead: self.DEAD,
                },
                self.JUMP: {
                    self.k_down: self.JUMP_ATTACK, self.l_down: self.JUMP_ATTACK,
                    self.comma_down: self.JUMP_ATTACK, self.period_down: self.JUMP_ATTACK,
                    self.land: self.IDLE, self.hit: self.HIT, self.dead: self.DEAD,
                },
                self.JUMP_DIAG: {
                    self.k_down: self.JUMP_DIAG_ATTACK, self.l_down: self.JUMP_DIAG_ATTACK,
                    self.comma_down: self.JUMP_DIAG_ATTACK, self.period_down: self.JUMP_DIAG_ATTACK,
                    self.land: self.IDLE, self.hit: self.HIT, self.dead: self.DEAD,
                },
                self.JUMP_DIAG_ATTACK: {
                    self.k_down: self.JUMP_DIAG_ATTACK, self.l_down: self.JUMP_DIAG_ATTACK,
                    self.comma_down: self.JUMP_DIAG_ATTACK, self.period_down: self.JUMP_DIAG_ATTACK,
                    self.land: self.IDLE, self.dead: self.DEAD,
                },
                self.JUMP_ATTACK: {
                    self.k_down: self.JUMP_ATTACK, self.l_down: self.JUMP_ATTACK,
                    self.comma_down: self.JUMP_ATTACK, self.period_down: self.JUMP_ATTACK,
                    self.land: self.IDLE, self.hit: self.HIT, self.dead: self.DEAD,
                },
                self.HIT: {
                    self.end_hit: self.IDLE, self.dead: self.DEAD,
                },
                self.DEAD: {
                },
                self.GUARD: {
                    self.block_up: self.IDLE,
                    self.dead: self.DEAD,
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

    def get_bb(self):
        return self.x-30, self.y-30,self.x+30,self.y+30

    def get_action_bb(self):
        """현재 상태(특히 공격)의 sx,sy,sw,sh을 이용해 AABB 반환. 없으면 get_bb() 폴백."""
        STAND_H = 92

        st = getattr(self.state_machine, 'cur_state', None)

        # 공격 계열 상태인지 확인 (attack_frames 존재 여부로 판단)
        if st and hasattr(st, 'attack_frames') and getattr(st, 'attack_type', None) is not None:
            try:
                attack_type = st.attack_type
                frames = st.attack_frames.get(attack_type)
                if not frames:
                    return self.get_bb()

                # 상태에 frame이 없을 수 있으므로 상태.frame -> self.frame 폴백
                raw_frame = getattr(st, 'frame', None)
                if raw_frame is None:
                    raw_frame = getattr(self, 'frame', 0.0)
                idx = min(int(raw_frame), len(frames) - 1)

                sx, sy, sw, sh = frames[idx]

                # 기본 보정: 대부분의 draw()에서 사용한 보정 재현
                base_w = frames[0][2] if frames else sw
                base_h = frames[0][3] if frames else sh
                dx = ((sw - base_w) * 0.5) * getattr(self, 'face_dir', 1)

                # 앉기/점프 계열은 세로 앵커를 STAND_H 기준으로 처리
                cls_name = st.__class__.__name__.lower()
                if 'crouch' in cls_name or 'sit' in cls_name or 'jump' in cls_name:
                    draw_x = self.x + dx
                    draw_y = (self.y - STAND_H * 0.5) + sh * 0.5
                else:
                    dy = (sh - base_h) * 0.5
                    draw_x = self.x + dx
                    draw_y = self.y + dy

                left = draw_x - sw * 0.5
                right = draw_x + sw * 0.5
                bottom = draw_y - sh * 0.5
                top = draw_y + sh * 0.5
                return left, bottom, right, top
            except Exception:
                # 실패 시 폴백
                return self.get_bb()

        # 가드 등 별도 상태(혹은 기본)일 경우 기존 바운딩박스 사용
        return self.get_bb()

    def handle_collision(self, group, other):
        if group == 'p1:p2':
            if getattr(other, 'is_attacking', False):
                if not hasattr(other, '_hit_targets'):
                    other._hit_targets = set()
                if self not in other._hit_targets:
                    other._hit_targets.add(self)
                    self.take_damage(5)

    def take_damage(self, amount):
        if getattr(self, 'is_guarding', False):
            return
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            if getattr(self, 'state_machine', None) and getattr(self.state_machine, 'cur_state', None) is not getattr(
                    self, 'DEAD', None):
                self.state_machine.handle_state_event(('DEAD', None))
        if not getattr(self, 'is_guarding', False):
            if getattr(self, 'state_machine', None) and getattr(self.state_machine, 'cur_state', None) is not getattr(
                    self, 'HIT', None):
                self.state_machine.handle_state_event(('HIT', None))
        else:
            pass