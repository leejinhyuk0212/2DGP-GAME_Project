import game_framework
from pico2d import *
import title_mode
import play_mode
import time

# 이미지, 선택 커서 위치/속도, 이동 플래그
image = None
select = None
select_x = 250
select_y = 300
GRID_X = 92
GRID_Y = 105
SCREEN_W, SCREEN_H = 800, 600

blink_interval = 0.5
blink_visible = True
last_blink_time = 0.0
blink_paused = False


def init():
    global image, select, select_x, select_y
    image = load_image('characterselect.png')   # 배경 (예: 1024x1024)
    select = load_image('select1.png')          # 커서 또는 스프라이트 시트
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
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(title_mode)
            elif event.key == SDLK_SPACE:
                game_framework.change_mode(play_mode)
            elif event.key == SDLK_LEFT:
                select_x -= GRID_X
                blink_visible = True
                blink_paused = True
            elif event.key == SDLK_RIGHT:
                select_x += GRID_X
                blink_visible = True
                blink_paused = True
            elif event.key == SDLK_UP:
                select_y += GRID_Y
                blink_visible = True
                blink_paused = True
            elif event.key == SDLK_DOWN:
                select_y -= GRID_Y
                blink_visible = True
                blink_paused = True

            # 화면 경계 제한 (선택 커서가 화면 밖으로 나가지 않도록)
            select_x = max(0, min(SCREEN_W, select_x))
            select_y = max(0, min(SCREEN_H, select_y))

def pause():
    pass

def resume():
    pass