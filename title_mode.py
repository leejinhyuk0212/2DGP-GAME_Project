from idlelib.run import get_message_lines
import game_framework
from pico2d import *
import select_mode

def init():
    global image
    image = load_image('title.png')

def finish():
    global image
    del image

def update():
    pass

def paues():
    pass

def resume():
    pass

def draw():
    clear_canvas()
    image.draw(400,300,800,600)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(select_mode)

def pause():
    pass

def resume():
    pass