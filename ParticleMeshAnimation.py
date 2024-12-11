import pygame
from pygame.locals import *
import random
import math

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
    

# This function finds the closest particles to itself and returns a tuple of the particle indecies. 
# EX: if we are finding the 3 closest particles and there are 5 particles the returned will be
# (5, 3, 2,    5, 4, 3,   1, 4, 5,    2, 5, 1,   2, 3, 4)
#    p1^          p2^       p3^         p4^         p5^
# The first 3 correspond to the first particle, second 3 to the second particle... etc.
# So the closest to particle 1 is particles 5, 3, and 2, in order of closest to farthest
    def findClosestParticle(self, listOfPoints, numOfConnections):
        # listOfPoints contains all particles X and Y positions as tuples, 
        # numOfConnections the number of particles we are finding closest to origin partilce
        
        listOfClosest = []

        # List of closest will contain the origin particle number, followed by the distance to every other particle
        # Two loops are created to create this distance from each particle to every other particle (Not efficient yet)
        #
        # If the origin particle and the target particle are the same, "10000" is appended as the distance so make sure when it is sorted, it is placed last
        # This is done to maintain order, without it I get outOfIndex errors
        # 
        # List of Closest will look like this when finished:
        # [(0, (0, 10000), (1, 166.2), (2, 102.5), (3, 502.0)),     (1, (0, 166.2), (1, 10000), (2, 402.1), (3, 255.0)),     (3, ...)]
        # Inital number indicates the particles number, the following tuples are the particle # its measuring to, followed by the distance from the origin particle

        for i in range(len(listOfPoints)):
            listOfDistances = []

            for j in range(len(listOfPoints)):
                if i != j:

                    point1X = (listOfPoints[i])[0]
                    point1Y = (listOfPoints[i])[1]

                    point2X = (listOfPoints[j])[0]
                    point2Y = (listOfPoints[j])[1]

                    deltaX = (point1X - point2X)
                    deltaY = (point1Y - point2Y)
                    distance = round(math.sqrt((deltaX)**2 + (deltaY)**2), 1)
                    #angle = round(deltaY/deltaX, 3) # gets the angle from origin particle to target particle if necessary
                    listOfDistances.append((j, distance))
                else:
                    listOfDistances.append((j, 10000))

            # After obtaining all distances from each particle to each other particle, I then sort it by the distances

            listOfDistances = sorted(listOfDistances, key=lambda tup: tup[1])
            listOfClosest.append((i, listOfDistances))
        
        # eachParticleClosest is to simplfy the returned array to remove excess information
        # This new list only contains the particle #s of closest particles in distance order of closest to farthest 

        eachParticlesClosest = []
        for i in range(len(listOfClosest)):
            for j in range(numOfConnections):
                eachParticlesClosest.append((((listOfClosest[i])[1])[j])[0])

        # Return the shortened list in the format listed at the start of this function
        
        return(eachParticlesClosest)


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
                particle = Particle(particleColor, random.randint(0, screenXsize), random.randint(0, screenYsize), random.randint(1,10), (random.random() / 5), random.uniform(0, 2 * math.pi))
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

            numOfConnections = 2
            eachParticlesClosest = particle.findClosestParticle(allParticlePositionsXY, numOfConnections)
            allPolygons = []
            
            for i in range(len(allParticlePositionsXY)):
                polygonPoints = [allParticlePositionsXY[i]]
                for j in range(numOfConnections):
                    polygonPoints.append(allParticlePositionsXY[eachParticlesClosest[(i * numOfConnections) + j]])
                allPolygons.append(polygonPoints)
            heightRatio = 255/screenYsize

            for i in range(len(allPolygons)):
                pygame.draw.polygon(screen, ((((allPolygons[i])[0])[1]) * heightRatio, 0 , 0), allPolygons[i])
            
            
            # alreadyDrawn = []
            # for i in range(particleCount - 1):
            #     for j in range(particleCount):

            #         if(allParticlePositionsXY[i] != allParticlePositionsXY[j] and ((i,j) or (j,i) not in alreadyDrawn)):
            #             pygame.draw.line(screen, lineColor, allParticlePositionsXY[i], allParticlePositionsXY[j], 2)
            #             alreadyDrawn.append((i,j))


            for i in range(particleCount): 
                particle = particles[i]
                particle.update()
                particle.drawPoints()
            pygame.display.update()



if __name__ == "__main__":
    main()