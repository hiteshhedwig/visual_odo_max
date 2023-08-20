import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import curses

# Importing transformation modules
from roadmap.foundation.src.transformation.translation import apply_translation_to_points
from roadmap.foundation.src.transformation.rotation import rotate_points_based_on_key
from roadmap.foundation.src.transformation.scaling import apply_scaling_to_points

class PlayCube:
    def __init__(self):
        """Initialize the cube's vertices and edges."""
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
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7]
        ]

    def draw_cube(self):
        """Render the cube using OpenGL."""
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def play(self, stdscr):
        """Main loop to handle user input and render the cube."""
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)

        # Curses settings for non-blocking input
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.nodelay(1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            stdscr.addstr(1, 0, "Please press a key: ")
            user_input = stdscr.getch()
            time.sleep(0.01)

            # Handle user input for transformations
            if user_input != -1:
                asciival = user_input
                user_input = str(chr(user_input))

                # Handle rotation based on arrow keys
                if asciival in [curses.KEY_DOWN, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_LEFT]:
                    self.vertices = rotate_points_based_on_key(1, axis_key=asciival, points=self.vertices)

                # Handle translation based on WASD keys
                translations = {
                    "d": (0.02, 0, 0),
                    "a": (-0.02, 0, 0),
                    "w": (0, 0.02, 0),
                    "s": (0, -0.02, 0)
                }
                if user_input in translations:
                    self.vertices = apply_translation_to_points(*translations[user_input], self.vertices)

                # Handle scaling based on M and N keys
                scalings = {
                    "m": (1.2, 1.2, 1.2),
                    "n": (0.8, 0.8, 0.8)
                }
                if user_input in scalings:
                    self.vertices = apply_scaling_to_points(*scalings[user_input], self.vertices)

            stdscr.refresh()

            # Render the cube
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_cube()
            pygame.display.flip()
            pygame.time.wait(10)

if __name__ == "__main__":
    play = PlayCube()
    curses.wrapper(play.play)
