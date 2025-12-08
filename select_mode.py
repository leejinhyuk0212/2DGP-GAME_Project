import game_framework
from pico2d import *
import title_mode
import play_mode

# 이미지, 선택 커서 위치/속도, 이동 플래그
image = None
select = None
select_x = 250
select_y = 300
SELECT_SPEED = 300  # 픽셀/초

move_left = move_right = move_up = move_down = False

def init():
    global image, select, select_x, select_y
    image = load_image('characterselect.png')   # 배경 (예: 1024x1024)
    select = load_image('select1.png')          # 커서 또는 스프라이트 시트
    # 필요 시 select2 = load_image('select2.png')
    select_x, select_y = 180, 250

def finish():
    global image, select
    if image:
        del image
        image = None
    if select:
        del select
        select = None

def update():
    global select_x, select_y
    dt = 1.0 / 60.0
    dx = dy = 0
    if move_left:
        dx -= SELECT_SPEED * dt
    if move_right:
        dx += SELECT_SPEED * dt
    if move_up:
        dy += SELECT_SPEED * dt
    if move_down:
        dy -= SELECT_SPEED * dt

    select_x += dx
    select_y += dy

    select_x = max(0, min(800, select_x))
    select_y = max(0, min(600, select_y))

def draw():
    clear_canvas()
    if image:
        image.draw(400, 300, 800, 600)
    if select:
        select.draw(select_x, select_y, 50, 50)
    update_canvas()

def handle_events():
    global move_left, move_right, move_up, move_down
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(title_mode)
            elif event.key == SDLK_SPACE:
                game_framework.change_mode(play_mode)
            elif event.key == SDLK_LEFT:
                move_left = True
            elif event.key == SDLK_RIGHT:
                move_right = True
            elif event.key == SDLK_UP:
                move_up = True
            elif event.key == SDLK_DOWN:
                move_down = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                move_left = False
            elif event.key == SDLK_RIGHT:
                move_right = False
            elif event.key == SDLK_UP:
                move_up = False
            elif event.key == SDLK_DOWN:
                move_down = False

def pause():
    pass

def resume():
    pass