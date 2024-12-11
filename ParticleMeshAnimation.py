import pygame
from pygame.locals import *
import random
import math
import numpy as np
from scipy.spatial import Delaunay

# Set all initial conditions & initialize pygame

pygame.init()
clock = pygame.time.Clock()
particleColor = (0, 0, 0)
screenXsize = 1000
screenYsize = 800
screen = pygame.display.set_mode((screenXsize, screenYsize)) 
pygame.display.set_caption('Floating Point Animation') 
pygame.display.update()

# Define how many particles will be in the animation
particleCount = 100

# For new colors on each run
offsetR = random.randint(0, 100) # Red
offsetG = random.randint(0, 100) # Green
offsetB = random.randint(0, 100) # Blue



# Create particle class
# This class will handle the particle creation, drawing, and movement
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
        self.angle += ((random.random() - .5) / 5)
        self.x += round(self.speed * math.cos(self.angle), 1)
        self.y += round(self.speed * math.sin(self.angle), 1)


# Allows the current X and Y coordiantes to be accessed
    def getXY(self):
        return (round(self.x, 1), round(self.y, 1))


# DrawPoints redraws the particles every frame in their new positions
    def drawPoints(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, 0)

# Creates the Delaunay Triangle Mesh using SciPy
    def getTriangleMeshFromPoints(self, allPoints):
        return (Delaunay(allPoints))
    
# Uses the Delaunay Triangle Mesh to draw the mesh onto the screen, then colors each triangle according to its height
    def drawTriangleMesh(self, allTriangles, allPoints, heightRatio):
        for triangle in allTriangles.simplices:
            trinaglePoints = allPoints[triangle]
            averageYofTriangle = 0
            
            for points in trinaglePoints:
                averageYofTriangle += points[1]
            
            averageYofTriangle = (averageYofTriangle / len(trinaglePoints)) * heightRatio
            pygame.draw.polygon(screen, 
                               (averageYofTriangle + offsetR, # Red
                               averageYofTriangle + offsetG,  # Green
                               averageYofTriangle + offsetB), # Blue
                               trinaglePoints)




# The main loads the screen, and appends all the particles based on particleCount
# While running loop gets all particle positions and (x, y) tuples, calls getTriangleMeshFromPoints, then calls DrawTriangleMesh
# Finally it updates all positions of the particles and updates the screen, then repeats all steps

def main():
    # Set up initial conditions before animation loop
    running = True

    # Add corner particles
    particles = []
    particles.append(Particle(particleColor, 0, 0, 1, 0, 0))
    particles.append(Particle(particleColor, screenXsize, 0, 1, 0, 0))
    particles.append(Particle(particleColor, 0, screenYsize, 1, 0, 0))
    particles.append(Particle(particleColor, screenXsize, screenYsize, 1, 0, 0))
    
    for i in range(particleCount - 4): # Removes 4 Corner particles from count
        particle = Particle(
            particleColor,                  # Color
            random.randint(0, screenXsize), # X location
            random.randint(0, screenYsize), # Y location
            random.randint(1,8),            # Size
            (random.random() * .5),         # Speed
            random.uniform(0, 2 * math.pi)) # Angle
        particles.append(particle)
        particle.drawPoints()



    # animation loop 
    while running: 
     
        for event in pygame.event.get(): # For loop through the event queue             
            if event.type == pygame.QUIT: # Check for QUIT event
                running = False

        clock.tick(60) # 60 FPS

        allParticlePositions = [] # Get intial list of all X and Y coordinates as tuples: (x, y)

        for i in range(particleCount): # Calling all particle positions 
            particle = particles[i]
            allParticlePositions.append(particle.getXY())
        
        allTriangles = particle.getTriangleMeshFromPoints(allParticlePositions) # Create mesh out of allParticlePositions using Delaunay
        heightRatio = 150/screenYsize # Create screen height ratio for proper triangle coloring
        particle.drawTriangleMesh(allTriangles, np.array(allParticlePositions), heightRatio) # Draw the mesh

        for i in range(particleCount): # Update the screen
            particle = particles[i]
            particle.update()
            particle.drawPoints()
        pygame.display.update()

if __name__ == "__main__":
    main()
