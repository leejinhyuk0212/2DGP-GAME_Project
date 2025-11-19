from pico2d import *
import game_framework
import select_mode
import game_world
from ryu import Ryu
from ken import Ken
from map import Map1
from countdown import CountdownSprite
from round_fight import RoundFightOverlay
from hp_bar import HealthBar

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_mode)
        elif not round_fight.visible:  # ✅ 연출 중 아닐 때만 입력 전달
            p1.handle_event(event)

def init():
    global p1, p2, map, countdown, round_fight, hp_bar, hp_bar2
    p1 = Ryu()
    p1.select = 1
    p2= Ken()
    p2.select = 2
    map = Map1()
    hp_bar = HealthBar(p1)
    hp_bar2 = HealthBar(p2)
    map.set_target(p1)
    map.set_target(p2)
    p1.set_camera(map)

    game_world.add_object(map, 0)
    game_world.add_object(p1, 1)
    game_world.add_object(p2, 1)
    game_world.add_object(hp_bar, 2)
    game_world.add_object(hp_bar2, 2)

    round_fight = RoundFightOverlay()
    countdown = CountdownSprite()

    game_world.add_collision_pair('p1:p2', p1, None)
    game_world.add_collision_pair('p1:p2', None, p2)

def finish():
    pass

def update():
    global countdown
    frame_time = game_framework.frame_time
    round_fight.update(frame_time)
    countdown.update(frame_time)

    if not round_fight.visible:
        game_world.update()
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    round_fight.draw()
    countdown.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass
