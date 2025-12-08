import game_framework
from pico2d import *
import title_mode
import play_mode
import time

# 이미지, 선택 커서 위치/속도, 이동 플래그
image = None
select = None
select_x = 180
select1_pos = False
select_y = 250
select2_pos = False
GRID_X = 92
GRID_Y = 105
SCREEN_W, SCREEN_H = 800, 600

MIN_X = 180
MAX_X = 180 + GRID_X * 5
MAX_Y = 250
MIN_Y = 145

blink_interval = 0.5
blink_visible = True
last_blink_time = 0.0
blink_paused = False

RYU_POSITION = (180, 250)
KEN_POSITION = (180, 250 - GRID_Y)


def init():
    global image, select, select_x, select_y
    image = load_image('characterselect.png')
    select = load_image('select1.png')
    select2 = load_image('select2.png')
    select_x, select_y = 180, 250
    blink_visible = True
    last_blink_time = time.time()
    blink_paused = False

def finish():
    global image, select
    if image:
        del image
        image = None
    if select:
        del select
        select = None

def update():
    global blink_visible, last_blink_time
    now = time.time()
    if now - last_blink_time >= blink_interval:
        blink_visible = not blink_visible
        last_blink_time = now

def draw():
    clear_canvas()
    if image:
        image.draw(400, 300, 800, 600)
    if select and blink_visible:
        select.draw(select_x, select_y, 50, 50)
    update_canvas()

def handle_events():
    global select_x, select_y, blink_visible, last_blink_time, blink_paused
    global select1_pos
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(title_mode)
            elif event.key == SDLK_SPACE:
                if not select1_pos:
                    if select_x == RYU_POSITION[0] and select_y == RYU_POSITION[1]:
                        play_mode.selected_p1 = 'Ryu'
                        select1_pos = True
                        game_framework.change_mode(play_mode)
                    elif select_x == KEN_POSITION[0] and select_y == KEN_POSITION[1]:
                        play_mode.selected_p1 = 'Ken'
                        select1_pos = True
                        game_framework.change_mode(play_mode)
            elif event.key == SDLK_LEFT:
                if select_x > MIN_X:
                    select_x -= GRID_X
                    blink_visible = True
                    blink_paused = True
                    last_blink_time = time.time()
            elif event.key == SDLK_RIGHT:
                if select_x < MAX_X:
                    select_x += GRID_X
                    blink_visible = True
                    blink_paused = True
                    last_blink_time = time.time()
            elif event.key == SDLK_UP:
                if select_y < MAX_Y:
                    select_y += GRID_Y
                    blink_visible = True
                    blink_paused = True
                    last_blink_time = time.time()
            elif event.key == SDLK_DOWN:
                if select_y > MIN_Y:
                    select_y -= GRID_Y
                    blink_visible = True
                    blink_paused = True
                    last_blink_time = time.time()


def pause():
    pass

def resume():
    pass