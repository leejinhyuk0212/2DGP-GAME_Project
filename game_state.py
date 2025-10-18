class GameState:
    current = None   # 현재 활성화된 씬

    def change(new_scene):
        GameState.current = new_scene
