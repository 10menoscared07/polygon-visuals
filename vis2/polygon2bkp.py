import math
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
    def __init__(self, pos:vec2, radius:float=10):
        self.pos = pos 
        self.radius = radius
        self.pi = 3.1415

        self.dof = 10
        self.buffer = 30
        self.thickness = 4

        # self.times = [random.randint(4,5) for _ in range(self.dof+1)]
        self.times = [4,4,5,4,4,5,4,4,4,5,4]
        self.rotators = [Timer(self.times[i]) for i in range(len(self.times))]

        self.rotatingTimer = Timer(5)
        self.roundsDone = 0

        
        self.factor = 1/4

        self.polygons = []
        
        self.color = vec3(200, 200, 200)
        self.backColor = vec3(30,30,30)

        self.generate()

    def setPoints(self, coords):
        self.coords = coords
        self.generate()
    
    def generate(self):
        pass

    def update(self, dt):
        # self.rotatingTimer.update(dt)
        # if self.rotatingTimer.isOver():
        #     self.rotatingTimer.reset()
        # x = 0
        for timer in self.rotators:
            timer.update(dt)
            if timer.isOver():
                timer.reset()
                # x += 1
                # print(self.roundsDone)
            
            # self.roundsDone += math.floor(x/self.dof)
            # print(self.roundsDone)

    def draw(self, window):
        dof = 0
        while dof <= self.dof:
            
            radius = self.radius - dof*self.buffer
            numSides = (self.dof - dof ) + 3
            angleDiff = 2*self.pi/numSides
            # pygame.draw.circle(window, self.color, self.pos, radius, self.thickness-2)

            points = []
            for i in range(numSides):
                angle = angleDiff*i
                x = self.pos.x + radius*math.cos(angle)
                y = self.pos.y + radius*math.sin(angle)
                points.append((x,y))

            pygame.draw.polygon(window, self.color, points, self.thickness)


            ## drawing the rotaing part
            percentDone = self.rotators[dof].percentCompleted()
            rotatorAngle = 2*self.pi*percentDone

            i = math.floor(rotatorAngle/angleDiff)
            prev = vec2(self.pos.x + radius*math.cos(angleDiff*i),  self.pos.y + radius*math.sin(angleDiff*i))
            after = vec2(self.pos.x + radius*math.cos(angleDiff*(i+1)),  self.pos.y + radius*math.sin(angleDiff*(i+1)))

            # if dof == 3:
            #     pygame.draw.circle(window, (2,20,200), prev, 8)
            #     pygame.draw.circle(window, (2,20,200), after, 8)

            rotatorPos = prev + (after-prev)*(((percentDone)*numSides) -i)

            pygame.draw.circle(window, (200,20,20), rotatorPos, 8)

            dof += 1



res = vec2(1280, 720)

window = pygame.display.set_mode(res)

clock = pygame.time.Clock()
dt = 1/60
fps = 60

h = Handler(res//2, 320)


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


        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                h.dof += 1
            else:
                h.dof -= 1
            print(h.dof)

    h.draw(window)
    h.update(dt)

    pygame.display.flip()