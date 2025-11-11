from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT
from state_machine import StateMachine

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

    def enter(self, e):
        self.ryu.wait_time = get_time()
        self.ryu.dir = 0


    def exit(self, e):
        pass

    def do(self):
        self.ryu.frame = (self.ryu.frame + 1) % 3  # 0,1,2 순환
        self.ryu.idle_frames = [6, 7, 8]
        if get_time() - self.ryu.wait_time > 3:
            self.ryu.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        frame_idx = self.ryu.idle_frames[self.ryu.frame]
        frame_width = 46  # 평균값 또는 7~9번 프레임 폭 기준
        frame_height = 92
        frame_x = [328, 384, 456][self.ryu.frame]  # 각 프레임 x 좌표
        frame_y = 1096  # y좌표는 동일

        if self.ryu.face_dir == 1:  # 오른쪽
            self.ryu.image.clip_draw(frame_x, frame_y, frame_width, frame_height, self.ryu.x, self.ryu.y)
        else:  # 왼쪽
            self.ryu.image.clip_composite_draw(frame_x, frame_y, frame_width, frame_height, 0, 'h', self.ryu.x,
                                               self.ryu.y, frame_width, frame_height)

class Run:
    def __init__(self, ryu):
        self.ryu = ryu

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.ryu.dir = self.ryu.face_dir = 1
        elif left_down(e) or right_up(e):
            self.ryu.dir = self.ryu.face_dir = -1

    def exit(self, e):
        if space_down(e):
            self.ryu.fire_ball()

    def do(self):
        self.ryu.frame = (self.ryu.frame + 1) % 8
        self.ryu.x += self.ryu.dir * 5

    def draw(self):
        if self.ryu.face_dir == 1: # right
            self.ryu.image.clip_draw(self.ryu.frame * 100, 100, 100, 100, self.ryu.x, self.ryu.y)
        else: # face_dir == -1: # left
            self.ryu.image.clip_draw(self.ryu.frame * 100, 0, 100, 100, self.ryu.x, self.ryu.y)


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