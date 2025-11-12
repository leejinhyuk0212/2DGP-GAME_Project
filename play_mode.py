from pico2d import *
import game_framework
import select_mode
import game_world
from ryu import Ryu
from map import Map1
from countdown import CountdownSprite

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
    global ryu, map, countdown
    ryu = Ryu()
    map = Map1()
    map.set_target(ryu)
    ryu.set_camera(map)

    game_world.add_object(map, 0)
    game_world.add_object(ryu, 1)

    countdown = CountdownSprite()

def finish():
    pass

def update():
    global countdown
    frame_time = game_framework.frame_time
    countdown.update(frame_time)
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    countdown.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass
