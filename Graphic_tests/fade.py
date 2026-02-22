import pygame,math
pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
W, H = screen.get_size()
clock = pygame.time.Clock()

gravity = 0.2
friction = 0.96

class Node:
    def __init__(self, x, y, pinned=False):
        self.x, self.y = x, y
        self.ox, self.oy = x, y
        self.pinned = pinned
        self.vol = 0

class Link:
    def __init__(self, n1, n2):
        self.n1, self.n2 = n1, n2
        self.dist = math.hypot(n1.x - n2.x, n1.y - n2.y)
        self.active = True

def create_phantom():
    nodes, links = [], []
    cols, rows = 60, 60
    spacing = 30
    start_x = (W - cols*spacing)//2
    for y in range(rows):
        for x in range(cols):
            nodes.append(Node(start_x + x*spacing, 50 + y*spacing, y == 0))
    for y in range(rows):
        for x in range(cols):
            if x < cols - 1: 
                links.append(Link(nodes[y*cols+x], nodes[y*cols+x+1]))
            if y < rows - 1: 
                links.append(Link(nodes[y*cols+x], nodes[(y+1)*cols+x]))
    return nodes, links
nodes, links = create_phantom()

running = True
while running:
    fade = pygame.Surface((W,H))
    fade.fill((0,0,0))
    fade.set_alpha(80)
    screen.blit(fade, (0,0))

    nx, ny = pygame.mouse.get_pos()
    n_down = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: nodes, links = create_phantom()
        if event.type == pygame.MOUSEMOTION:
            for n in nodes:
                d = math.hypot(n.x - nx, n.y - ny)
                if d < 48:
                    n.x += (n.x - nx) * 0.1
                    n.y += (n.y - ny) * 0.1

    for n in nodes:
        if not n.pinned:
            vx  = (n.x - n.ox) * friction
            vy = (n.y - n.oy) * friction
            n.ox, n.oy = n.x, n.y
            n.x += vx
            n.y += vy + gravity
            n.vol = math.hypot(vx, vy)

    for _ in range(4):
        for l in links:
            if not l.active: continue
            dx, dy = l.n2.x - l.n1.x, l.n2.y - l.n1.y
            d = math.hypot(dx, dy) + 0.001

            if d > l.dist * 3.0 or (n_down and math.hypot((l.n1.x+l.n2.x)/2 - nx, (l.n1.y+l.n2.y)/2 - ny) < 15):
                l.active = False; continue
            
            diff = (l.dist - d) / d * 0.5
            if not l.n1.pinned: l.n1.x -= dx * diff; l.n1.y -= dy * diff
            if not l.n2.pinned: l.n2.x += dx * diff; l.n2.y += dy * diff
    for l in links:
        if l.active:
            speed = (l.n1.vol + l.n2.vol) / 2

            brightness = min(255, int(speed * 50))
            if brightness > 10:
                color = (brightness, brightness, brightness+20 if brightness < 235 else 255)
                pygame.draw.line(screen, color, (l.n1.x, l.n1.y), (l.n2.x, l.n2.y), 1)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()