import pygame, sys
from typing import List
pygame.init()

vec2 = pygame.math.Vector2

res = vec2(1280, 720)

window = pygame.display.set_mode(res)

class Mirror:
    def __init__(self, start, end):
        self.startPos = start
        self.endPos = end
        self.midPos = (self.startPos + self.endPos)//2
        self.length = (start-end).length()

        self.alongDir = self.endPos - self.startPos
        self.alongDir: vec2
        self.alongDir.normalize_ip()
        
        self.perpDir = self.alongDir.rotate(90)


        self.pivotPos = self.midPos
        self.pivotRadius = 10


        self.reflected = False

    def getDistance(self, pos):
        l1 = (self.startPos - pos).length()
        l2 = (self.endPos - pos).length()

        numerator = (self.endPos.x - self.startPos.x)*(self.startPos.y - pos.y) - (self.startPos.x-pos.x)*(self.endPos.y - self.startPos.y)
        numerator = abs(numerator)

        return numerator/self.length
    
    def getNormalUnit(self):
        return self.perpDir

    def draw(self, window):
        pygame.draw.line(window, (200,200,200), self.startPos, self.endPos, 3)
        pygame.draw.line(window, (200,200,200), self.midPos, self.midPos+self.perpDir*20, 3)

    def update(self, dt):
        pass

class Ray:
    def __init__(self, pos:vec2, speed:float=800):
        self.startPos = pos
        self.speed = speed

        self.velocity =  vec2(speed, 0)

    
        self.pos = pos

        self.path = []

    def reset(self):
        self.path.clear()
        self.pos = self.startPos.copy()
        self.velocity =  vec2(self.speed, 0)

    def update(self, dt:float, mirrors:List[Mirror]):
        self.pos += self.velocity * dt

        self.path.append(self.pos.copy())

        for mirror in mirrors:
            if not mirror.reflected:
                print(mirror.getDistance(self.pos))
                if mirror.getDistance(self.pos) <= 4:
                    n = mirror.getNormalUnit()
                    ei  = self.velocity.normalize()
                    angle = -2*ei.dot(n)
                    er =  ei + (angle)*n

                    self.velocity = er * self.speed
                    mirror.reflected = True

    def draw(self, window):
        for pos in self.path:
            pygame.draw.circle(window, (200, 30, 30), pos, 5)


mirrors = []

mirrors.append(Mirror(vec2(100,100), vec2(300,300)))
mirrors.append(Mirror(vec2(100,500), vec2(400,650)))
mirrors.append(Mirror(vec2(600,100), vec2(700,300)))



ray = Ray(vec2(10,200))

clock = pygame.time.Clock()
dt = 1/60
fps = 60

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
                ray.reset()


    for mirror in mirrors:
        mirror.draw(window)
        mirror.update(dt)

    ray.update(dt, mirrors)
    ray.draw(window)

    pygame.display.flip()