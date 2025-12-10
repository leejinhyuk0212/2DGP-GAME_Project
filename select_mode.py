import game_framework
from pico2d import *
import title_mode
import play_mode
import time
import os

image = None
select = None
select2 = None

select_x = 180
select_y = 250

select1_pos = False
select2_pos = False
selection_phase = 1

p1_marker = False
p1_marker_pos = (0, 0)

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

blink2_interval = 0.5
blink2_visible = True
last_blink_time2 = 0.0
blink2_paused = True

RYU_POSITION = (180, 250)
KEN_POSITION = (180, 250 - GRID_Y)

bgm=None
def init():
    global image, select, select2, select_x, select_y
    global blink_visible, last_blink_time, blink_paused
    global select1_pos, select2_pos, selection_phase
    global p1_marker, p1_marker_pos
    global blink2_visible, last_blink_time2, blink2_paused
    global bgm

    image = load_image('characterselect.png')
    select = load_image('select1.png')
    bgm = load_music(('sound/select_mode_bgm.mp3'))
    bgm.set_volume(32)
    bgm.repeat_play()
    try:
        select2 = load_image('select2.png')
    except:
        select2 = None

    select_x, select_y = RYU_POSITION
    blink_visible = True
    last_blink_time = time.time()
    blink_paused = False

    blink2_visible = True
    last_blink_time2 = time.time()
    blink2_paused = True

    select1_pos = False
    select2_pos = False
    selection_phase = 1

    p1_marker = False
    p1_marker_pos = (0, 0)

def finish():
    global image, select, select2, bgm
    if image:
        del image
        image = None
    if select:
        del select
        select = None
    if select2:
        del select2
        select2 = None
    bgm = None

def update():
    global blink_visible, last_blink_time
    global blink2_visible, last_blink_time2

    now = time.time()
    if not blink_paused:
        if now - last_blink_time >= blink_interval:
            blink_visible = not blink_visible
            last_blink_time = now

    if selection_phase == 2 and not blink2_paused:
        if now - last_blink_time2 >= blink2_interval:
            blink2_visible = not blink2_visible
            last_blink_time2 = now

def draw():
    clear_canvas()
    if image:
        image.draw(400, 300, 800, 600)

    if p1_marker and select is not None:
        select.draw(p1_marker_pos[0], p1_marker_pos[1], 50, 50)

    if selection_phase == 1 and select and blink_visible:
        select.draw(select_x, select_y, 50, 50)

    if selection_phase == 2 and select2 and blink2_visible:
        select2.draw(select_x, select_y, 50, 50)

    update_canvas()

def handle_events():
    global select_x, select_y, blink_visible, last_blink_time, blink_paused
    global select1_pos, select2_pos, selection_phase
    global p1_marker, p1_marker_pos
    global blink2_paused, last_blink_time2, blink2_visible
    global bgm2

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(title_mode)

            elif event.key == SDLK_SPACE:
                if selection_phase == 1 and not select1_pos:
                    if select_x == RYU_POSITION[0] and select_y == RYU_POSITION[1]:
                        play_mode.selected_p1 = 'Ryu'
                        bgm2 = load_wav('sound/ch_select.wav')
                        bgm2.set_volume(32)
                        bgm2.play(1)
                        select1_pos = True
                    elif select_x == KEN_POSITION[0] and select_y == KEN_POSITION[1]:
                        play_mode.selected_p1 = 'Ken'
                        play_mode.selected_p1 = 'Ryu'
                        bgm2 = load_wav('sound/ch_select.wav')
                        bgm2.set_volume(32)
                        bgm2.play(1)
                        select1_pos = True

                    if select1_pos:
                        p1_marker = True
                        p1_marker_pos = (select_x, select_y)
                        blink_paused = True
                        blink_visible = True
                        selection_phase = 2
                        select_x, select_y = RYU_POSITION
                        blink2_paused = False
                        blink2_visible = True
                        last_blink_time2 = time.time()

                elif selection_phase == 2 and not select2_pos:
                    if select_x == RYU_POSITION[0] and select_y == RYU_POSITION[1]:
                        play_mode.selected_p2 = 'Ryu'
                        select2_pos = True
                    elif select_x == KEN_POSITION[0] and select_y == KEN_POSITION[1]:
                        play_mode.selected_p2 = 'Ken'
                        select2_pos = True

                    if select2_pos:
                        game_framework.change_mode(play_mode)

            elif event.key == SDLK_LEFT:
                if select_x > MIN_X and selection_phase in (1, 2):
                    select_x -= GRID_X
                    if selection_phase == 1:
                        blink_visible = True
                        blink_paused = True
                        last_blink_time = time.time()
                    else:
                        blink2_visible = True
                        blink2_paused = False
                        last_blink_time2 = time.time()

            elif event.key == SDLK_RIGHT:
                if select_x < MAX_X and selection_phase in (1, 2):
                    select_x += GRID_X
                    if selection_phase == 1:
                        blink_visible = True
                        blink_paused = True
                        last_blink_time = time.time()
                    else:
                        blink2_visible = True
                        blink2_paused = False
                        last_blink_time2 = time.time()

            elif event.key == SDLK_UP:
                if select_y < MAX_Y and selection_phase in (1, 2):
                    select_y += GRID_Y
                    if selection_phase == 1:
                        blink_visible = True
                        blink_paused = True
                        last_blink_time = time.time()
                    else:
                        blink2_visible = True
                        blink2_paused = False
                        last_blink_time2 = time.time()

            elif event.key == SDLK_DOWN:
                if select_y > MIN_Y and selection_phase in (1, 2):
                    select_y -= GRID_Y
                    if selection_phase == 1:
                        blink_visible = True
                        blink_paused = True
                        last_blink_time = time.time()
                    else:
                        blink2_visible = True
                        blink2_paused = False
                        last_blink_time2 = time.time()

    select_x = max(MIN_X, min(MAX_X, select_x))
    select_y = max(MIN_Y, min(MAX_Y, select_y))

def pause():
    pass

def resume():
    pass