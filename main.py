from pico2d import *
from title import Initial_Screen
from game_state import GameState

open_canvas(800, 600)
running = True

# 초기 화면 설정
GameState.change(Initial_Screen())

while running:
    for e in get_events():
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            running = False
        else:
            GameState.current.handle_event(e)

    GameState.current.draw()
    delay(0.01)

close_canvas()
