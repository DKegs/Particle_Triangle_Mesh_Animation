import pygame
from pygame.locals import *
import random
import math
import numpy as np
from scipy.spatial import Delaunay

# Set all initial conditions & initialize pygame

pygame.init()
clock = pygame.time.Clock()
backgroundColor = (104, 112, 152) 
particleColor = (0, 0, 0)
lineColor = (0, 255, 0)
screenXsize = 1000
screenYsize = 800
screen = pygame.display.set_mode((screenXsize, screenYsize)) 
pygame.display.set_caption('Floating Point Animation') 
screen.fill(backgroundColor) 
pygame.display.update()

# Define how many particles will be in the animation
particleCount = 50



# Create particle class
# This class will handle the particle movement
class Particle:
    def __init__(self, color: tuple , x: float, y: float, radius: float, speed: float, angle: float):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle

# Update is for moving the particle every frame, and bouncing off an edge if hit
    def update(self):
        if self.x < 0 or self.x > screenXsize:
            self.angle = math.pi - self.angle

        if self.y < 0 or self.y > screenYsize:
            self.angle = -self.angle

    # Uncomment the following code to wrap the screen instead of bouncing
        # if self.x < 0 or self.x > screenXsize:
        #     if self.x < 0:
        #         self.x = screenXsize
        #     else:
        #         self.x = 0

        # if self.y < 0 or self.y > screenYsize:
        #     if self.y < 0:
        #         self.y = screenYsize
        #     else:
        #         self.y = 0

    # Adds the proper movement each frame
        self.x += round(self.speed * math.cos(self.angle), 1)
        self.y += round(self.speed * math.sin(self.angle), 1)


# Allows the current X and Y coordiantes to be accessed
    def getXY(self):
        return (round(self.x, 1), round(self.y, 1))


# DrawPoints redraws the particles every frame in their new positions

    def drawPoints(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, 0)




# The main loads the screen, but waits to start the animation until the user presses the spacebar
# Once pressed, it loads the particles based on how many are set in the particleCount integer
# It then calls the particle class for drawing them on the screen and moving them accordingly
# The closest particles list is used to create the shapes between particles for the animation

def main():
    
    running = True
    # game loop 
    particleExists = False
    while running: 
    # for loop through the event queue   
        for event in pygame.event.get():       
            # Check for QUIT event       
            if event.type == pygame.QUIT: 
                running = False
        

        keys = pygame.key.get_pressed()

        
        if keys[pygame.K_SPACE]:
            particles = []
            for i in range(particleCount):
                particle = Particle(
                    particleColor,                  # Color
                    random.randint(0, screenXsize), # X location
                    random.randint(0, screenYsize), # Y location
                    random.randint(1,10),           # Size
                    (random.random() / 5),          # Speed
                    random.uniform(0, 2 * math.pi)) # Angle
                particles.append(particle)
                particle.drawPoints()
            particleExists = True
            

        if particleExists:
            clock.tick(60) # 60 FPS
            allParticlePositionsXY = []

            screen.fill(backgroundColor)
            for i in range(particleCount):  
                particle = particles[i]
                allParticlePositionsXY.append(particle.getXY())
            
            allPoints = np.array(allParticlePositionsXY)
            allTriangles = Delaunay(allPoints)
            heightRatio = 255/screenYsize
            
            for triangle in allTriangles.simplices:
                trinaglePoints = allPoints[triangle]
                averageYofTriangle = 0
                for points in trinaglePoints:
                    averageYofTriangle += points[1]
                averageYofTriangle = (averageYofTriangle / len(trinaglePoints)) * heightRatio
                pygame.draw.polygon(screen, (0, 0, averageYofTriangle), trinaglePoints)


            for i in range(particleCount): 
                particle = particles[i]
                particle.update()
                particle.drawPoints()
            pygame.display.update()

if __name__ == "__main__":
    main()
