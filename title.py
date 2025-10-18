from pico2d import (
    load_image, clear_canvas, update_canvas, get_canvas_width, get_canvas_height,
    SDL_KEYDOWN, SDLK_RETURN, SDLK_BACKSPACE
)
from game_state import GameState



class Initial_Screen:
    def __init__(self):
        self.image = load_image('title.png')

    def handle_event(self, e):
        # Enter 키 눌렀을 때 캐릭터 선택 화면으로 전환
        if e.type == SDL_KEYDOWN and e.key == SDLK_RETURN:
            GameState.change(CharacterSelect_Screen())
        return None

    def draw(self):
        clear_canvas()
        cw, ch = get_canvas_width(), get_canvas_height()
        self.image.draw(cw // 2, ch // 2, cw, ch)
        update_canvas()


# --------------------------- #
# 캐릭터 선택 화면 클래스     #
# --------------------------- #
class CharacterSelect_Screen:
    def __init__(self):
        self.image = load_image('characterselect.png')

    def handle_event(self, e):
        # Backspace 눌렀을 때 타이틀로 돌아가기
        if e.type == SDL_KEYDOWN and e.key == SDLK_BACKSPACE:
            GameState.change(Initial_Screen())
        return None

    def draw(self):
        clear_canvas()
        cw, ch = get_canvas_width(), get_canvas_height()
        self.image.draw(cw // 2, ch // 2, cw, ch)
        update_canvas()
