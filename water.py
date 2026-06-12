import pygame, random
import math as m
from pygame import *

class surface_water_particle():
    k = 0.04  # spring constant
    d = 0.08  # damping constant
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.target_y = y
        self.velocity = 0

    def update(self):
        x = self.y_pos - self.target_y              # displacement of "spring"
        a = -self.k * x - self.d * self.velocity    # unit of acceleration

        self.y_pos += self.velocity
        self.velocity += a

class water():
    def __init__(self, x_start, x_end, y_start, y_end, segment_length):
        self.springs = []
        self.final_pos_x = 400
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end - 10
        for i in range(int(x_end - x_start) // segment_length):
            self.springs.append(surface_water_particle(i * segment_length + x_start, y_end))

    def update(self, spread):
        passes = 4  # more passes = more splash spreading
        for i in range(len(self.springs)):
            self.springs[i].update() 

        leftDeltas = [0] * len(self.springs)
        rightDeltas = [0] * len(self.springs)
        for p in range(passes):  
            for i in range(0, len(self.springs) -1 ):
                if i > 0:  
                    leftDeltas[i] = spread * (self.springs[i].y_pos - self.springs[i - 1].y_pos)
                    self.springs[i - 1].velocity += leftDeltas[i]
                if i < len(self.springs) - 1:
                    rightDeltas[i] = spread * (self.springs[i].y_pos - self.springs[i + 1].y_pos)
                    self.springs[i + 1].velocity += rightDeltas[i]

            for i in range(0, len(self.springs) -1):
                if i > 0:
                    self.springs[i - 1].y_pos += leftDeltas[i]  # you were updating velocity here!
                if i < len(self.springs) - 1:
                    self.springs[i + 1].y_pos += rightDeltas[i]             
                
    def splash(self, index, speed):
        if index > 0 and index < len(self.springs):
            self.springs[index].velocity = speed
        # self.number_rod = abs((index-self.final_pos_x)/2)
        # self.index = int(index / self.final_pos_x * self.number_rod)
                
    def draw(self,surface,water_test,sw,sh,alp):
        alpha = 100-20
        water_surface = pygame.Surface((sw,sh))
        water_surface.fill((0,0,0,0))
        water_surface.set_colorkey((0,0,0,0))
        polygon_points = []
        polygon_points.append((self.x_start, self.y_start))
        for spring in range(len(self.springs)):
            polygon_points.append((water_test.springs[spring].x_pos, water_test.springs[spring].y_pos))
        polygon_points.append((water_test.springs[len(self.springs) - 1].x_pos, self.y_start))

        poly = pygame.draw.polygon(water_surface, (51,204,255), polygon_points)

        for spring in range(0,len(self.springs) - 1):
            pygame.draw.line(water_surface, (255,255,255), (water_test.springs[spring].x_pos, water_test.springs[spring].y_pos), (water_test.springs[spring + 1].x_pos, water_test.springs[spring + 1].y_pos), 2)
        
        water_surface.set_alpha(alp)
        return water_surface

# while True:
   
    
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#         if event.type == MOUSEBUTTONDOWN:
#             water_test.splash(50,100)

#     pygame.display.update()

#     clock.tick(60)
