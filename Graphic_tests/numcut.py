import pygame, math, random
pygame.init()

info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
font = pygame.font.SysFont('monospace', 32, bold=True)
clock = pygame.time.Clock()

cols, rows = 15, 20
spacing = 35
points = []
for y in range(rows):
    for x in range(cols):
        points.append({'x': x*spacing+(W-cols*spacing)//2, 'y': y*spacing +50,
                       'oldx': x*spacing + (W-cols+spacing)//2, 'oldy': y*spacing + 50,
                       'pinned': y==0
                       })
links = []

for y in range(rows):
    for x in range(cols):
        idx = y*cols+x
        if x < cols - 1:
            links.append({'p1': points[idx], 'p2': points[idx + 1], 'len': spacing})
        if y < rows - 1:
            links.append({'p1': points[idx], 'p2': points[idx + cols], 'len': spacing})

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
            for l in links[:]:
                if math.hypot(((l['p1']['x'] + l['p2']['x']) / 2 - mx), ((l['p1']['y'] + l['p2']['y']) / 2 - my)) < 25:
                    links.remove(l)

    for p in points:
        if not p['pinned']:
            vx, vy = (p['x'] - p['oldx']) * 0.95, (p['y'] - p['oldy']) * 0.95
            p['oldx'], p['oldy'] = p['x'], p['y']
            p['x'], p['y'] = p['x'] + vx, p['y'] + vy + 0.5
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[2]:
                if math.hypot(p['x'] - mx, p['y'] - my) < 20:
                    p['x'], p['y'] = mx, my
                    p['oldx'], p['oldy'] = mx, my


    for _ in range(3):
        for l in links:
            dx, dy = l['p1']['x'] - l['p2']['x'], l['p1']['y'] - l['p2']['y']
            dist = math.hypot(dx, dy)
            if dist == 0: continue
            f = (l['len'] - dist) / dist * 0.5
            if not l['p1']['pinned']: l['p1']['x'] += dx * f; l['p1']['y'] += dy * f
            if not l['p2']['pinned']: l['p2']['x'] -= dx * f; l['p2']['y'] -= dy * f

    for l in links:
        mid_x = (l['p1']['x'] + l['p2']['x']) / 2
        mid_y = (l['p1']['y'] + l['p2']['y']) / 2
        char = "1" if random.random() > 0.5 else "0"
        color = (0, 255, 255) if random.random() > 0.1 else (255, 0, 255)
        txt = font.render(char, True, color)
        screen.blit(txt, (mid_x - 5, mid_y - 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()