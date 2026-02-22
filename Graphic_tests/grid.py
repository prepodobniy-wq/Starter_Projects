import pygame,math
pygame.init()

s = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
W, H, clock = s.get_width(), s.get_height(), pygame.time.Clock()
P = [[x*20+W/4, y*20+100, x*20+W/4, y*20+100, y==0] for y in range(30) for x in range(50)]
S = [[i,i+1,1] for i in range(len(P)) if (i+1)%50] + [[i,i+50,1] for i in range(len(P)-50)]

while True:
    if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in pygame.event.get()): exit()

    s.fill((6,5,18))

    mx, my = pygame.mouse.get_pos()
    md = pygame.mouse.get_pressed()

    for p in P:
        if not p[4]:
            if md[0] and math.hypot(p[0]-mx, p[1]-my) < 30: p[0], p[1] = mx, my
            vx, vy = max(-20,min(20, (p[0]-p[2])*0.99)), max(-20, min(20, (p[1]-p[3])*0.99))
            p[2],p[3],p[0],p[1] = p[0], p[1], p[0]+vx, p[1]+vy+0.4
    for _ in range(6):
        for sk in [k for k in S if k[2]]:
            p1, p2 = P[sk[0]], P[sk[1]]
            dx, dy = p2[0]-p1[0], p2[1]-p1[1]
            d = math.hypot(dx, dy) or 0.1
            if d > 100 or (md[2] and math.hypot((p1[0]+p2[0])/2-mx, (p1[1]+p2[1])/2-my) < 15):
                sk[2] = 0; continue
            f = (20-d)/d*0.5
            if not p1[4]: p1[0]-=dx*f; p1[1]-=dy*f
            if not p2[4]: p2[0]+=dx*f; p2[1]+=dy*f
    for p1, p2, active in [k for k in S if k[2]]:
        pygame.draw.line(s, (0, 255, 150), (P[p1][0], P[p1][1]), (P[p2][0], P[p2][1]),2)
    pygame.display.flip()
    clock.tick(60)
