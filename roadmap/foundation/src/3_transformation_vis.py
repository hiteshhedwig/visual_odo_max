import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import select
import sys
from roadmap.foundation.src.transformation.translation import *
from roadmap.foundation.src.transformation.rotation import *

class PlayCube(object):
    def __init__(self):
        self.vertices = [
                        [1, 1, -1],
                        [1, 1, 1],
                        [-1, 1, 1],
                        [-1, 1, -1],
                        [1, -1, -1],
                        [1, -1, 1],
                        [-1, -1, 1],
                        [-1, -1, -1]
                    ]
        
        self.edges = [
                        [0, 1],
                        [1, 2],
                        [2, 3],
                        [3, 0],
                        [4, 5],
                        [5, 6],
                        [6, 7],
                        [7, 4],
                        [0, 4],
                        [1, 5],
                        [2, 6],
                        [3, 7]
                    ]
    
    def draw_cube(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def play(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # glRotatef(1, 3, 1, 1)
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)  # 100ms timeout
            if ready:
                user_input = sys.stdin.readline().strip()
                print(f"You entered: {user_input}")
                # xyz for rotation
                if user_input == "x":
                    self.vertices = apply_rotation_to_pointarray(1, axis=user_input, points_arr = self.vertices)
                if user_input == "y":
                    self.vertices = apply_rotation_to_pointarray(1, axis=user_input, points_arr = self.vertices)
                if user_input == "z":
                    self.vertices = apply_rotation_to_pointarray(1, axis=user_input, points_arr = self.vertices)
                
                # wasd for translation
                if user_input == "d" :
                    self.vertices = apply_translation_to_pointarray(0.2,0,0,self.vertices)
                if user_input == "a" :
                    self.vertices = apply_translation_to_pointarray(-0.2,0,0,self.vertices)
                if user_input == "w":
                    self.vertices = apply_translation_to_pointarray(0,0.2,0,self.vertices)
                if user_input == "s":
                    self.vertices = apply_translation_to_pointarray(0,-0.2,0,self.vertices)


            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_cube()
            pygame.display.flip()
            pygame.time.wait(10)


if __name__ == "__main__":
    play = PlayCube()
    play.play()