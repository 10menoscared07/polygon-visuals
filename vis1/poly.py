import pygame, sys
from typing import List
pygame.init()



vec2 = pygame.math.Vector2


class Handler:
    def __init__(self, coords):
        self.coords = coords
        self.dof = 3

        self.polygons = []
        self.generate()
    
    def generate(self):
        self.polygons.clear()
        self.polygons.append((0, self.coords))

        dof = 1
        while dof <= self.dof:
            coords = self.polygons[dof-1][1]

            p = []
            for i in range(1, len(coords)):
                if not i == len(coords)-1:
                    f = coords[i-1]
                    n = coords[i]

                    p.append((f+n)//2)
                else:
                    f = coords[len(coords)-1]
                    n = coords[0]

                    p.append((f+n)//2)   


            self.polygons.append((dof, p))

    def draw(self, window):
        for poly in self.polygons:
            c = 255*(1-poly[0]/self.dof)
            pygame.draw.polygon(window, (c,c,c), poly[1])



res = vec2(1280, 720)

window = pygame.display.set_mode(res)

clock = pygame.time.Clock()
dt = 1/60
fps = 60

h = Handler(vec2(100, 200), vec2(400, 200), vec2(400, 400), vec2(100, 400))

while 1:
    window.fill((30,30,30))
    clock.tick(120)

    fps = clock.get_fps()

    dt = 1/fps if fps else 1/120

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                pass

    h.draw(window)

    pygame.display.flip()