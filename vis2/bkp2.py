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
        self.numSidesBase = 4
        self.thickness = 4

        self.baseLuminance = 30
        self.polygonColors = [[360*i/self.dof, 100, self.baseLuminance, 100] for i in range(self.dof + 1)]
        


        self.rotatorThickness = 5
        self.rotatorColor = [150]*3
        self.highlightRotatorColor = [255]*3
        # self.vertexColor = []


        # self.times = [random.randint(4,5) for _ in range(self.dof+1)]
        self.baseTime = 8
        self.times = [self.baseTime for _ in range(self.dof + 1)]
        self.times[1]+= 2
        self.times[5] += 2
        self.rotatingTime = [Timer(self.times[i]) for i in range(len(self.times))]



        self.rotatorData = [None for _ in range(self.dof + 1)]



        self.roundsDone = [0 for _ in range(self.dof + 1)]



    def update(self, dt):
        for i in range(len(self.rotatingTime)):
            timer = self.rotatingTime[i]
            timer.update(dt)

            if timer.isOver():
                timer.reset()

        ### checking if the rotator is hovered over

        mp = vec2(*pygame.mouse.get_pos())
        dist = (mp-self.pos).length()

        xDist = 0
        dof = self.dof
        while xDist <= dist:
            xDist += self.buffer
            dof -= 1
        dof += 1

        for color in self.polygonColors:
            color[2] = self.baseLuminance

        if dof >= 0 and dof <= self.dof:
            self.polygonColors[dof][2] = self.baseLuminance+20

            pygame.draw.circle(window, self.rotatorColor, self.rotatorData[dof][1], self.rotatorThickness, 2)
            pygame.draw.circle(window, self.rotatorColor, self.rotatorData[dof][2], self.rotatorThickness, 2)

            ### draw a line from origin
            # pygame.draw.line(window, self.rotatorColor, self.pos, self.rotatorData[dof][0], 2)



        

    def draw(self, window):
        dof = 0
        while dof <= self.dof:
            
            ### properties of current polygon
            circumRadius = self.radius - dof*self.buffer
            numSides = (self.dof - dof ) + self.numSidesBase
            centralAngle = 2*self.pi/numSides
            ### properties done

            ### drawing the polygonal path
            points = []
            for i in range(numSides):
                angle = centralAngle*i
                x = self.pos.x + circumRadius*math.cos(angle)
                y = self.pos.y + circumRadius*math.sin(angle)
                points.append((x,y))
            pygame.draw.polygon(window, pygame.Color.from_hsla(self.polygonColors[dof]), points, self.thickness)

            ### polygon drawn


            ## drawing the rotaing part
            percentDone = self.rotatingTime[dof].percentCompleted()
            angle = 2*self.pi*percentDone

            i = math.floor(angle/centralAngle) ## getting the id of nearest vertex

            lastVertex = vec2(self.pos.x + circumRadius*math.cos(centralAngle*i),  self.pos.y + circumRadius*math.sin(centralAngle*i))  ### the previous vertex
            nextVertex = vec2(self.pos.x + circumRadius*math.cos(centralAngle*(i+1)),  self.pos.y + circumRadius*math.sin(centralAngle*(i+1)))  ### the next vertex

            rotatorPos = lastVertex + (nextVertex - lastVertex)* (((percentDone)*numSides) -i) ### getting the actual position of the rotator on the basis of the current ablge it is present at!

            ### updating properties of this rotator in the list
            self.rotatorData[dof] = (rotatorPos, lastVertex, nextVertex, angle)



            ### check if the area is hovered:
            if self.polygonColors[dof][2] > self.baseLuminance:
                pygame.draw.circle(window, self.highlightRotatorColor, rotatorPos, self.rotatorThickness)
            else:
                pygame.draw.circle(window, self.rotatorColor, rotatorPos, self.rotatorThickness)


            ### increase the depth of field counter bruh (infinite loop)
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
            # print(h.dof)

    h.draw(window)
    h.update(dt)

    pygame.display.flip()