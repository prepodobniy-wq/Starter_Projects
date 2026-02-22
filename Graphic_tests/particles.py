import pygame, math, random
pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
W, H = screen.get_size()
clock = pygame.time.Clock()
particles = [[random.random()*W, random.random()*H, 0, 0] for _ in range(2500)]
running = True
while running:
    fade = pygame.Surface((W, H))
    fade.fill((2,4,10))
    fade.set_alpha(40)
    screen.blit(fade, (0,0))
    nx, ny = pygame.mouse.get_pos()
    n_down = pygame.mouse.get_pressed()

    for p in particles:
        dx, dy = nx-p[0], ny-p[1]
        dist_sq = dx*dx + dy*dy + 500
        dist = math.sqrt(dist_sq)
        force = 5000/dist_sq
        if n_down[0]: force *= 5
        if n_down[2]: force *= -10
        p[2] += (dx/dist) * force
        p[1] += (dy/dist) * force
        p[2] *= 0.98
        p[3] *= 0.98
        p[0] += p[2]
        p[1] += p[3]
        vel = math.sqrt(p[2]**2 + p[3]**2)
        color = (min(255, 50+vel*20), min(255, 20+vel*5), min(255, 100+vel*10))
        pygame.draw.line(screen, color, (p[0], p[1]), (p[0]-p[2], p[1]-p[3]), 1)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
