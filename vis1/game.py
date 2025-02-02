import pygame, sys
from typing import List
pygame.init()

def line_intersection(p1, p2, p3, p4):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    if denom == 0:
        return None  # Parallel lines, no intersection

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

    return (px, py)

vec2 = pygame.math.Vector2

res = vec2(1280, 720)

window = pygame.display.set_mode(res)

class Mirror:
    def __init__(self, start, end):
        self.startPos = start
        self.endPos = end
        self.midPos = (self.startPos + self.endPos)//2
        self.length = (start-end).length()

        self.lengthVec = self.endPos - self.startPos

        self.alongDir = self.endPos - self.startPos
        self.alongDir: vec2
        self.alongDir.normalize_ip()
        
        self.perpDir = self.alongDir.rotate(90)


        self.pivotPos = self.midPos
        self.pivotRadius = 10
        self.pivotHovered = False
        self.pivotHeld = False
        self.pivotOffset = vec2(0,0)

        self.pivotStartOffset = (-self.pivotPos + self.startPos).copy()

        self.anchorPos = self.endPos
        self.anchorRadius = 10
        self.anchorHovered = False
        self.anchorHeld = False

        self.reflected = False

    def getDistance(self, pos):
        l1 = (self.startPos - pos).length()
        l2 = (self.endPos - pos).length()

        numerator = (self.endPos.x - self.startPos.x)*(self.startPos.y - pos.y) - (self.startPos.x-pos.x)*(self.endPos.y - self.startPos.y)
        numerator = abs(numerator)

        return numerator/self.length
    
    def getEndPoints(self):
        return self.startPos, self.startPos + self.lengthVec

    def getNormalUnit(self):
        return self.perpDir

    def update(self, dt):
        mp = vec2(*pygame.mouse.get_pos())

        ### pivot point udate

        if (mp-self.pivotPos).length() <= self.pivotRadius:
            self.pivotHovered = True
        else:
            if not self.pivotHeld:
                self.pivotHovered = False

        if pygame.mouse.get_pressed()[0]:
            if self.pivotHovered and not self.pivotHeld:
                self.pivotHeld = True
                self.pivotOffset = (mp-self.pivotPos).copy()

        else:
            self.pivotHeld = False
            
        if self.pivotHeld:
            self.pivotPos = mp - self.pivotOffset
            self.startPos = self.pivotPos + self.pivotStartOffset
            self.anchorPos = self.startPos + self.lengthVec

        if not self.pivotHeld:
            self.pivotStartOffset = (-self.pivotPos + self.startPos).copy()

        ### anchor point related
        if (mp-self.anchorPos).length() <= self.anchorRadius:
            self.anchorHovered = True
        else:
            if not self.anchorHeld:
                self.anchorHovered = False

        if pygame.mouse.get_pressed()[0]:
            if self.anchorHovered and not self.anchorHeld:
                self.anchorHeld = True
                self.anchorOffset = (mp-self.anchorPos).copy()

        else:
            self.anchorHeld = False

        if self.anchorHeld:
            vec = mp - self.startPos
            self.lengthVec = vec.normalize() * self.length
            
            self.pivotPos = self.startPos + self.lengthVec//2
            self.anchorPos = self.startPos + self.lengthVec



    def draw(self, window):
        pygame.draw.line(window, (200,200,200), self.startPos, self.startPos + self.lengthVec, 3)
        

        if self.pivotHovered:
            pygame.draw.circle(window, (180, 180, 180), self.pivotPos, self.pivotRadius)
        pygame.draw.circle(window, (220,220,220), self.pivotPos, self.pivotRadius, width=3)


        if self.anchorHovered:
            pygame.draw.circle(window, (180, 180, 180), self.anchorPos, self.anchorRadius)
        pygame.draw.circle(window, (220,220,220), self.anchorPos, self.anchorRadius, width=3)
        
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

        # for mirror in mirrors:
        #     if not mirror.reflected:
        #         print(mirror.getDistance(self.pos))
        #         if mirror.getDistance(self.pos) <= 4:
        #             n = mirror.getNormalUnit()
        #             ei  = self.velocity.normalize()
        #             angle = -2*ei.dot(n)
        #             er =  ei + (angle)*n

        #             self.velocity = er * self.speed
        #             mirror.reflected = True

        # self.dof = 0
        # while self.dof < 8:
        #     for mirror
        #     self.dof += 1

    def draw(self, window):
        for pos in self.path:
            pygame.draw.circle(window, (200, 30, 30), pos, 5)


mirrors = []

mirrors.append(Mirror(vec2(100,100), vec2(300,300)))
# mirrors.append(Mirror(vec2(100,500), vec2(400,650)))
# mirrors.append(Mirror(vec2(600,100), vec2(700,300)))



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

    # ray.update(dt, mirrors)
    # ray.draw(window)

    pygame.display.flip()
    