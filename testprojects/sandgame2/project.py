from typing import List
import sys
import random
import pygame
import numpy as np

CELL_SIZE: int = 4
GRID_W: int = 200
GRID_H: int = 140
SIDEBAR_W: int = 220
WIDTH: int = GRID_W * CELL_SIZE + SIDEBAR_W
HEIGHT: int = GRID_H * CELL_SIZE
FPS: int = 60

# --- Материалы ---
EMPTY, WALL, SAND, WATER, OIL, FIRE, SMOKE, WOOD, LAVA, STONE, METAL, ICE, STEAM, ACID, GAS, GUNPOWDER, EXPLOSION = range(17)

ELEMENT_NAMES: dict[int, str] = {
    EMPTY: 'Пустота',
    WALL: 'Стена',
    SAND: 'Песок',
    WATER: 'Вода',
    OIL: 'Масло',
    FIRE: 'Огонь',
    SMOKE: 'Дым',
    WOOD: 'Дерево',
    LAVA: 'Лава',
    STONE: 'Камень',
    METAL: 'Металл',
    ICE: 'Лёд',
    STEAM: 'Пар',
    ACID: 'Кислота',
    GAS: 'Газ',
    GUNPOWDER: 'Порох',
    EXPLOSION: 'Взрыв'
}

COLORS: dict[int, tuple[int, int, int]] = {
    EMPTY: (0, 0, 0),
    WALL: (100, 100, 100),
    SAND: (194, 178, 128),
    WATER: (60, 120, 200),
    OIL: (40, 30, 30),
    FIRE: (255, 120, 0),
    SMOKE: (120, 120, 120),
    WOOD: (120, 70, 20),
    LAVA: (255, 50, 0),
    STONE: (130, 130, 130),
    METAL: (180, 180, 200),
    ICE: (180, 220, 255),
    STEAM: (200, 200, 255),
    ACID: (0, 255, 0),
    GAS: (180, 250, 180),
    GUNPOWDER: (50, 50, 50),
    EXPLOSION: (255, 255, 100)
}

SMOKE_RISE_PROB: float = 0.6
OIL_IGNITION_PROB: float = 0.5

# --- Сетка ---
def make_grid(default: int = EMPTY) -> List[List[int]]:
    return [[default for _ in range(GRID_W)] for _ in range(GRID_H)]

grid: List[List[int]] = make_grid()

# --- Утилиты ---
def in_bounds(y: int, x: int) -> bool:
    return 0 <= x < GRID_W and 0 <= y < GRID_H

def try_move(y: int, x: int, ny: int, nx: int) -> bool:
    if not in_bounds(ny, nx):
        return False
    if grid[ny][nx] == EMPTY:
        grid[ny][nx] = grid[y][x]
        grid[y][x] = EMPTY
        return True
    return False

# --- Обновление материалов ---

def update_sand(y: int, x: int, visited: List[List[bool]]) -> None:
    """Песок падает вниз или по диагонали (случайный порядок диагоналей)."""
    # вниз
    if try_move(y, x, y+1, x):
        visited[y+1][x] = True
        return
    # диагонали в случайном порядке
    diag = [(y+1, x-1), (y+1, x+1)]
    random.shuffle(diag)
    for ny, nx in diag:
        if try_move(y, x, ny, nx):
            visited[ny][nx] = True
            return
    visited[y][x] = True


def update_water(y: int, x: int, visited: List[List[bool]]) -> None:
    """Вода стремится вниз, потом в стороны (с некоторой рандомизацией)."""
    if try_move(y, x, y+1, x):
        visited[y+1][x] = True
        return
    options = [(y, x-1), (y, x+1), (y+1, x-1), (y+1, x+1)]
    random.shuffle(options)
    for ny, nx in options:
        if try_move(y, x, ny, nx):
            visited[ny][nx] = True
            return
    visited[y][x] = True


def update_oil(y: int, x: int, visited: List[List[bool]]) -> None:
    """Масло похоже на воду, но медленнее и легче загорается."""
    if try_move(y, x, y+1, x):
        visited[y+1][x] = True
        return
    options = [(y, x-1), (y, x+1)]
    random.shuffle(options)
    for ny, nx in options:
        if try_move(y, x, ny, nx):
            visited[ny][nx] = True
            return
    visited[y][x] = True


def update_acid(y: int, x: int, visited: List[List[bool]]) -> None:
    """Кислота течёт как вода и иногда разрушает соседние материалы."""
    if try_move(y, x, y+1, x):
        visited[y+1][x] = True
        return
    options = [(y, x-1), (y, x+1), (y+1, x-1), (y+1, x+1)]
    random.shuffle(options)
    for ny, nx in options:
        if try_move(y, x, ny, nx):
            visited[ny][nx] = True
            return
    # разъедание соседей
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = y+dy, x+dx
            if not in_bounds(ny, nx):
                continue
            target = grid[ny][nx]
            # не трогаем саму кислоту, воду, огонь, пар и пустоту
            if target not in (EMPTY, ACID, WATER, FIRE, SMOKE, STEAM):
                if random.random() < 0.08:
                    grid[ny][nx] = EMPTY
    visited[y][x] = True


def update_gunpowder(y: int, x: int, visited: List[List[bool]]) -> None:
    """Порох ведёт себя как песок, но при контакте с огнём взрывается."""
    # движение как у песка
    if try_move(y, x, y+1, x):
        visited[y+1][x] = True
        return
    diag = [(y+1, x-1), (y+1, x+1)]
    random.shuffle(diag)
    for ny, nx in diag:
        if try_move(y, x, ny, nx):
            visited[ny][nx] = True
            return
    # если рядом огонь — взрыв
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = y+dy, x+dx
            if in_bounds(ny, nx) and grid[ny][nx] == FIRE:
                grid[y][x] = EXPLOSION
                visited[y][x] = True
                return
    visited[y][x] = True


def update_explosion(y: int, x: int, visited: List[List[bool]]) -> None:
    """Взрыв — одноразовый эффект, распространяет огонь/пустоту в радиусе."""
    radius = 2
    for dy in range(-radius, radius+1):
        for dx in range(-radius, radius+1):
            ny, nx = y+dy, x+dx
            if not in_bounds(ny, nx):
                continue
            # вероятность уничтожения в зависимости от расстояния
            dist2 = dy*dy + dx*dx
            if dist2 <= radius*radius:
                if random.random() < max(0.3, 1.0 - dist2/(radius*radius)):
                    # некоторые материалы становятся огнём, другие просто удаляются
                    if grid[ny][nx] in (WOOD, OIL, GUNPOWDER):
                        grid[ny][nx] = FIRE
                    else:
                        grid[ny][nx] = EMPTY
    # центральная клетка исчезает
    grid[y][x] = EMPTY
    visited[y][x] = True


def update_gas(y: int, x: int, visited: List[List[bool]]) -> None:
    """Газ поднимается и может воспламениться рядом с огнём."""
    # поднимается с некоторой вероятностью
    if random.random() < 0.8 and try_move(y, x, y-1, x):
        visited[y-1][x] = True
        return
    # рассеивается
    if random.random() < 0.002:
        grid[y][x] = EMPTY
        visited[y][x] = True
        return
    # воспламенение рядом
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = y+dy, x+dx
            if in_bounds(ny, nx) and grid[ny][nx] == FIRE:
                grid[y][x] = EXPLOSION
                visited[y][x] = True
                return
    visited[y][x] = True


def update_steam(y: int, x: int, visited: List[List[bool]]) -> None:
    """Пар поднимается и иногда конденсируется в воду."""
    if try_move(y, x, y-1, x):
        visited[y-1][x] = True
        return
    if random.random() < 0.012:
        grid[y][x] = WATER
    visited[y][x] = True


def update_ice(y: int, x: int, visited: List[List[bool]]) -> None:
    """Лёд тает при контакте с высокими температурами."""
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = y+dy, x+dx
            if in_bounds(ny, nx) and grid[ny][nx] in (FIRE, LAVA):
                grid[y][x] = WATER
                visited[y][x] = True
                return
    visited[y][x] = True


def update_lava(y: int, x: int, visited: List[List[bool]]) -> None:
    """Лава течёт, превращает воду в пар и поджигает легковоспламеняющиеся материалы."""
    if try_move(y, x, y+1, x):
        visited[y+1][x] = True
        return
    options = [(y, x-1), (y, x+1)]
    random.shuffle(options)
    for ny, nx in options:
        if try_move(y, x, ny, nx):
            visited[ny][nx] = True
            return
    # взаимодействия с соседями
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = y+dy, x+dx
            if not in_bounds(ny, nx):
                continue
            if grid[ny][nx] == WATER:
                grid[y][x] = STONE
                grid[ny][nx] = STEAM
            elif grid[ny][nx] in (WOOD, OIL, GUNPOWDER):
                grid[ny][nx] = FIRE
    visited[y][x] = True


def update_fire(y: int, x: int, visited: List[List[bool]]) -> None:
    """Огонь поднимается, образует дым, поджигает соседей (соседние материалы)."""
    # пытается подняться
    if random.random() < SMOKE_RISE_PROB and try_move(y, x, y-1, x):
        visited[y-1][x] = True
        return
    # шанс превратиться в дым
    if random.random() < 0.02:
        grid[y][x] = SMOKE
        visited[y][x] = True
        return
    # распространение огня на воспламеняемые материалы
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = y+dy, x+dx
            if not in_bounds(ny, nx):
                continue
            if grid[ny][nx] in (OIL, WOOD, GAS, GUNPOWDER):
                if random.random() < OIL_IGNITION_PROB:
                    grid[ny][nx] = FIRE
    visited[y][x] = True


def update_smoke(y: int, x: int, visited: List[List[bool]]) -> None:
    """Дым поднимается и рассеивается."""
    if random.random() < SMOKE_RISE_PROB and try_move(y, x, y-1, x):
        visited[y-1][x] = True
        return
    if random.random() < 0.01:
        grid[y][x] = EMPTY
    visited[y][x] = True

# --- Шаг симуляции ---
def step_simulation() -> None:
    """Выполняет один шаг симуляции, корректно вызывает update_* и помечает visited."""
    visited: List[List[bool]] = [[False]*GRID_W for _ in range(GRID_H)]
    # идём снизу вверх, чтобы гравитация шла корректно
    for y in range(GRID_H-1, -1, -1):
        xs = list(range(GRID_W))
        # рандомизация направления обхода по x для уменьшения артефактов
        if random.random() < 0.5:
            xs.reverse()
        for x in xs:
            if visited[y][x]:
                continue
            cell = grid[y][x]
            # вызываем соответствующую функцию обновления
            if cell == SAND:
                update_sand(y, x, visited)
            elif cell == WATER:
                update_water(y, x, visited)
            elif cell == OIL:
                update_oil(y, x, visited)
            elif cell == LAVA:
                update_lava(y, x, visited)
            elif cell == FIRE:
                update_fire(y, x, visited)
            elif cell == SMOKE:
                update_smoke(y, x, visited)
            elif cell == ACID:
                update_acid(y, x, visited)
            elif cell == GUNPOWDER:
                update_gunpowder(y, x, visited)
            elif cell == EXPLOSION:
                update_explosion(y, x, visited)
            elif cell == GAS:
                update_gas(y, x, visited)
            elif cell == STEAM:
                update_steam(y, x, visited)
            elif cell == ICE:
                update_ice(y, x, visited)
            else:
                # неподвижные материалы/прочее — пометить как посещённые
                visited[y][x] = True

def step_simulation():
    visited: List[List[bool]] = [[False]*GRID_W for _ in range(GRID_H)]
    for y in range(GRID_H-1, -1, -1):
        xs = list(range(GRID_W))
        if random.random() < 0.5:
            xs.reverse()
        for x in xs:
            if visited[y][x]:
                continue
            cell = grid[y][x]
            if cell == SAND:
                update_sand(y, x, visited)
            elif cell == WATER:
                update_water(y, x, visited)
            elif cell == OIL:
                update_oil(y, x, visited)
            elif cell == LAVA:
                update_lava(y, x, visited)
            elif cell == FIRE:
                update_fire(y, x, visited)
            elif cell == SMOKE:
                update_smoke(y, x, visited)
            elif cell == ACID:
                update_acid(y, x, visited)
            elif cell == GUNPOWDER:
                update_gunpowder(y, x, visited)
            elif cell == EXPLOSION:
                update_explosion(y, x, visited)
            elif cell == GAS:
                update_gas(y, x, visited)
            elif cell == STEAM:
                update_steam(y, x, visited)
            elif cell == ICE:
                update_ice(y, x, visited)

# --- Рисование и управление ---
def paint_circle(cx, cy, radius, material):
    r2 = radius*radius
    for dy in range(-radius, radius+1):
        y = cy + dy
        if y < 0 or y >= GRID_H:
            continue
        for dx in range(-radius, radius+1):
            x = cx + dx
            if x < 0 or x >= GRID_W:
                continue
            if dx*dx + dy*dy <= r2:
                grid[y][x] = material


def draw_grid(surface):
    for y in range(GRID_H):
        for x in range(GRID_W):
            color = COLORS[grid[y][x]]
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            surface.fill(color, rect)


def clear():
    for y in range(GRID_H):
        for x in range(GRID_W):
            grid[y][x] = EMPTY


def handle_events(paused, brush, brush_size):
    running = True
    step = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_ESCAPE, pygame.K_q}:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_c:
                clear()
            elif event.key == pygame.K_n and paused:
                step = True
            elif event.key == pygame.K_LEFTBRACKET:
                brush_size = max(1, brush_size-1)
            elif event.key == pygame.K_RIGHTBRACKET:
                brush_size = min(40, brush_size+1)
    return running, paused, brush, brush_size, step

# --- UI для выбора материала ---
def draw_sidebar(screen, font, brush, brush_size, paused, clock):
    sidebar_rect = pygame.Rect(GRID_W*CELL_SIZE, 0, SIDEBAR_W, HEIGHT)
    pygame.draw.rect(screen, (30, 30, 30), sidebar_rect)

    info = [
        f'FPS: {int(clock.get_fps())}',
        f'Кисть: {ELEMENT_NAMES.get(brush, brush)}',
        f'Размер кисти: {brush_size}',
        f'Пауза: {paused}',
    ]
    for i, line in enumerate(info):
        surf = font.render(line, True, (220, 220, 220))
        screen.blit(surf, (GRID_W*CELL_SIZE + 10, 10 + i*20))

    # Кнопки выбора материала
    y_offset = 120
    for mat, name in ELEMENT_NAMES.items():
        rect = pygame.Rect(GRID_W*CELL_SIZE + 10, y_offset, 80, 20)
        pygame.draw.rect(screen, COLORS[mat], rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            brush = mat
        text = font.render(name, True, (0, 0, 0))
        screen.blit(text, (GRID_W*CELL_SIZE + 100, y_offset))
        y_offset += 25
    return brush

# --- Главный цикл ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Falling Sand MOD — Python')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 16)

    running, paused, brush, brush_size = True, False, SAND, 4

    while running:
        running, paused, brush, brush_size, step = handle_events(paused, brush, brush_size)

        mx, my = pygame.mouse.get_pos()
        grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE
        buttons = pygame.mouse.get_pressed()
        if mx < GRID_W * CELL_SIZE:  # рисовать только в области поля
            if buttons[0]:
                paint_circle(grid_x, grid_y, brush_size, brush)
            if buttons[2]:
                paint_circle(grid_x, grid_y, brush_size, EMPTY)

        if step or not paused:
            step_simulation()

        draw_grid(screen)
        brush = draw_sidebar(screen, font, brush, brush_size, paused, clock)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
