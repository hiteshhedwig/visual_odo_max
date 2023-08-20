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
from roadmap.foundation.src.transformation.scaling import *
import curses

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

    def play(self, stdscr):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        curses.cbreak()  # Get input char-by-char instead of line-by-line
        stdscr.keypad(True)
        stdscr.nodelay(1)  # Make getch() non-blocking

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # glRotatef(1, 3, 1, 1)
            stdscr.addstr(1, 0, "Please press a key (you have 100ms): ")
            # xyz for rotation
            user_input = stdscr.getch()
            time.sleep(0.01)  # 100ms delay

            if user_input != -1:  
                print("pressed ", user_input)
                asciival = user_input
                user_input=str(chr(user_input))
                # arrow keys for rotation
                if asciival == curses.KEY_DOWN:
                    self.vertices = rotate_points_based_on_key(1, axis_key=asciival, points = self.vertices)
                if asciival == curses.KEY_RIGHT:
                    self.vertices = rotate_points_based_on_key(1, axis_key=asciival, points = self.vertices)
                if asciival == curses.KEY_UP:
                    self.vertices = rotate_points_based_on_key(1, axis_key=asciival, points = self.vertices)
                if asciival == curses.KEY_LEFT:
                    self.vertices = rotate_points_based_on_key(1, axis_key=asciival, points = self.vertices)

                # wasd for translation
                if user_input == "d" :
                    self.vertices = apply_translation_to_points(0.02,0,0,self.vertices)
                if user_input == "a" :
                    self.vertices = apply_translation_to_points(-0.02,0,0,self.vertices)
                if user_input == "w":
                    self.vertices = apply_translation_to_points(0,0.02,0,self.vertices)
                if user_input == "s":
                    self.vertices = apply_translation_to_points(0,-0.02,0,self.vertices)

                # m,n for scaling!
                if user_input == "m" :
                    self.vertices = apply_scaling_to_points(1.2,1.2,1.2,self.vertices)
                if user_input == "n" :
                    self.vertices = apply_scaling_to_points(0.8,0.8,0.8,self.vertices)

            stdscr.refresh()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_cube()
            pygame.display.flip()
            pygame.time.wait(10)


    


if __name__ == "__main__":
    play = PlayCube()
    curses.wrapper(play.play)