import random
import pygame, sys
from typing import List
pygame.init()


def clamp(val, mini, maxi):
    if val >= maxi:
        return maxi
    if val <= mini:
        return mini
    return val


class Interpolate:
    @staticmethod
    def lerp(final, initial, time, duration):
        return initial + (final-initial)*clamp(time/duration, 0, 1)
    
    @staticmethod
    def lerpNorm(final, initial, time):
        return initial + (final-initial)*clamp(time, 0, 1)

    @staticmethod
    def easeInOutNorm(final, initial, time):
        # Ease-in-out function
        if time < 0.5:
            # Ease-in phase
            value = initial + (final - initial) * (2 * time * time)
        else:
            # Ease-out phase
            value = initial + (final - initial) * (1 - pow(-2 * time + 2, 2) / 2)
        
        return value
    
class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.timer = 0
        self.finsied = False
    
    def update(self, deltaTime):
        self.timer += deltaTime
        if self.timer >= self.duration:
            self.finsied = True

    def percentCompleted(self):
        return clamp(self.timer/self.duration, 0, 1)

    def isOver(self):
        return self.finsied
    
    def end(self):
        self.timer = 0
        self.finsied = True

    def reset(self):
        self.timer = 0
        self.finsied = False


vec2 = pygame.math.Vector2
vec3 = pygame.math.Vector3


class Handler:
    def __init__(self, coords):
        self.coords = coords
        self.dof = 10
        
        self.factor = 1/4

        self.polygons = []
        self.generate()
        self.color = vec3(200, 200, 200)
        self.backColor = vec3(30,30,30)

    def setPoints(self, coords):
        self.coords = coords
        self.generate()
    
    def generate(self):
        self.polygons.clear()
        self.polygons.append((0, self.coords))

        dof = 1
        while dof <= self.dof:
            coords = self.polygons[dof-1][1]

            p = []
            for i in range(len(coords)):
                
                try:
                    f = coords[(i+1)]
                    
                    n = coords[i]
                    length = n-f

                    p.append((f+ length*self.factor))
                except:
                    f = coords[0]
                    
                    n = coords[-1]
                    length = n-f

                    p.append((f+ length*self.factor))

            self.polygons.append((dof, p))
            dof += 1

    def draw(self, window):
        for poly in self.polygons:
            color  = (self.color) + (self.backColor - self.color)*(poly[0]/self.dof)
            pygame.draw.polygon(window, color, poly[1])

class Dot:
    def __init__(self, pos):
        self.pos =pos

        self.baseRadius = 8
        self.bufferRadius = 4
        self.radius = 8
        self.thickness = 2
        self.color = (200,200,200)
        self.hoverFill = [50]*3
        self.hoverOutline = [240]*3

        self.isHovered = False
        self.beingDragged = False


    def draw(self, window):
        if not self.isHovered:
            pygame.draw.circle(window, self.color, self.pos, self.radius, self.thickness)
        elif self.isHovered:
            pygame.draw.circle(window, self.hoverFill, self.pos, self.radius)
            pygame.draw.circle(window, self.hoverOutline, self.pos, self.radius, self.thickness)

    def isColliding(self, pos):
        if (self.pos-pos).length() <= self.radius:
            return True
        return False

    def update(self, dt):
        self.mousePos = vec2(*pygame.mouse.get_pos())

        if self.isColliding(self.mousePos):
            self.isHovered = True
        else:
            self.isHovered = False

        if self.beingDragged:
            self.pos = self.mousePos - self.offset
            self.isHovered = True


        if self.isHovered:
            self.radius = self.baseRadius + self.bufferRadius
        else:
            self.radius = self.baseRadius

        if pygame.mouse.get_pressed()[0] and self.isHovered:
            if not self.beingDragged:
                self.offset = self.mousePos - self.pos

            self.beingDragged = True
        else:
            self.beingDragged = False



    def drawUpdate(self, window, dt):
        self.update(dt)
        self.draw(window)


res = vec2(1280, 720)

window = pygame.display.set_mode(res)

clock = pygame.time.Clock()
dt = 1/60
fps = 60

h = Handler([vec2(100, 200), vec2(400, 200), vec2(450,300), vec2(500, 400), vec2(100, 400)])

rect = pygame.Rect(0,0,450, 350)
rect.center= res//2

dots = [Dot(vec2(*rect.topleft)), Dot(vec2(*rect.topright)), Dot(vec2(*rect.bottomright)), Dot(vec2(*rect.bottomleft))]

targetColor = vec3(random.randint(0, 25)*10, random.randint(0, 25)*10, random.randint(0, 25)*10)
startColor = h.color

changeColorTimer = Timer(1)
alternatingColor = True

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
                dots.append(Dot(vec2(500,500)))

            if event.key == pygame.K_SPACE:
                for dot in dots:
                    points.append(dot.pos)
                h.setPoints(points)

            if event.key == pygame.K_UP:
                h.dof += 1
                h.generate()
            if event.key == pygame.K_DOWN:
                h.dof -= 1
                h.generate()
            if event.key == pygame.K_c:
                # h.color = vec3(random.randint(0, 25)*10, random.randint(0, 25)*10, random.randint(0, 25)*10)
                alternatingColor = not alternatingColor


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                dots.append(Dot(vec2(*event.pos)))

        elif event.type == pygame.MOUSEWHEEL:
            if event.y >0 :
                h.factor += 0.01
                if h.factor >= 1:
                    h.factor -= 1
            if event.y < 0 :
                h.factor -= 0.01
                if h.factor <= 0:
                    h.factor += 1

    h.draw(window)

    for dot in dots:
        dot.update(window)
        dot.draw(window)
    
    points = []

    for dot in dots:
        points.append(dot.pos)
    h.setPoints(points)

    ### alternating color 
    if alternatingColor:
        changeColorTimer.update(dt)

        h.color = Interpolate.lerpNorm(targetColor, startColor, changeColorTimer.percentCompleted())
        # print(h.color)

        if changeColorTimer.isOver():
            changeColorTimer.reset()
            targetColor = vec3(random.randint(0, 25)*10, random.randint(0, 25)*10, random.randint(0, 25)*10)
            startColor = h.color


    pygame.display.flip()