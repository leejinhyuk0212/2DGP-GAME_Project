world = [[], [], []] # layers for game objects
collision_pairs = {}

def add_object(o, depth):
    world[depth].append(o)

def add_objects(ol, depth):
    world[depth] += ol

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if _collide_objects(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def _collide_objects(a, b):
    a_boxes = _possible_bbs(a)
    b_boxes = _possible_bbs(b)

    for ab in a_boxes:
        for bb in b_boxes:
            if ab is None or bb is None:
                continue
            if _bb_overlap(ab, bb):
                return True
    return False

def _possible_bbs(o):
    bbs = []
    try:
        if hasattr(o, 'get_action_bb'):
            try:
                ab = o.get_action_bb()
                if ab:
                    bbs.append(ab)
            except Exception:
                pass
    except Exception:
        pass
    try:
        bb = o.get_bb()
        if bb:
            bbs.append(bb)
    except Exception:
        pass
    return bbs

def _bb_overlap(a_bb, b_bb):
    left_a, bottom_a, right_a, top_a = a_bb
    left_b, bottom_b, right_b, top_b = b_bb

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    raise Exception("World 에 존재하지 않는 오브젝트를 지우려고 시도함")


def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()