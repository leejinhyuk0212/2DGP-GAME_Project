from pico2d import *
import game_framework
import select_mode
import game_world
from ryu import Ryu
from map import Map1

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_mode)
        else:
            ryu.handle_event(event)

def init():
    global ryu
    global map
    ryu=Ryu()
    map=Map1()
    map.set_target(ryu)
    ryu.set_camera(map)

    game_world.add_object(ryu, 1)
    game_world.add_object(map, 0)

def finish():
    pass

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()



def pause():
    pass

def resume():
    pass