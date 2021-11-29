from collections import deque
from random import random

import pygame as pg


def get_rect(x, y):
    return x * TITLE + 1, y * TITLE + 1, TITLE - 2, TITLE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


cols, rows = 25, 15
TITLE = 60

pg.init()
sc = pg.display.set_mode([cols * TITLE, rows * TITLE])
clock = pg.time.Clock()

grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]

graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

start = (0, 0)
queue = deque([start])
visited = {start: None}
cur_node = start

while True:
    sc.fill(pg.Color('black'))
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TITLE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]

    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]

    # BFS logic
    if queue:
        cur_node = queue.popleft()
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node

    # draw path
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TITLE, border_radius=TITLE // 3)
        path_segment = visited[path_segment]

    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), border_radius=TITLE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TITLE // 3)

    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(7)
