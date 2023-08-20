import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import curses
import time

# Importing transformation modules
from roadmap.foundation.src.transformation.translation import apply_translation_to_points, translate_points_based_on_mouse_movement_
from roadmap.foundation.src.transformation.rotation import rotate_points_based_on_key, rotate_points_based_on_mouse_movement_
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

    def rotate_points_based_on_mouse_movement(self, dx, dy, vertices):
        print("DX ", dx)
        print("DY ", dy)
        if dx > 0 and dy == 0:
            self.vertices = rotate_points_based_on_key(1, axis_key=curses.KEY_RIGHT, points=vertices)
            return self.vertices
        if dx < 0 and dy == 0:
            self.vertices = rotate_points_based_on_key(1, axis_key=curses.KEY_LEFT, points=vertices)
            return self.vertices
        if dx == 0:
            return self.vertices
        
    def play(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)

        # Initial mouse positions
        init_x, init_y = None, None

        init_x_tr, init_y_tr = None, None

        last_click_time = 0
        DOUBLE_CLICK_THRESHOLD = 0.5  # 500 milliseconds

        double_click_mode = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                # Mouse button down event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left button
                        current_time = time.time()
                        if current_time - last_click_time < DOUBLE_CLICK_THRESHOLD:
                            double_click_mode = not double_click_mode
                        last_click_time = current_time

                        init_x, init_y = event.pos
                    elif event.button in [4, 5]:  # Scroll wheel
                        if event.button == 4:  # Scroll up
                            self.vertices = apply_scaling_to_points(1.1, 1.1, 1.1, self.vertices)
                        else:  # Scroll down
                            self.vertices = apply_scaling_to_points(0.9, 0.9, 0.9, self.vertices)

                # Mouse double click and drag!
                if double_click_mode:
                    print("Double click mode is on. Drag to move the cube. Rotation disabled")
                    # Mouse motion event for translation
                    if event.type == pygame.MOUSEMOTION and init_x is not None and init_y is not None:
                            cur_x, cur_y = event.pos
                            dx_t, dy_t = init_x - cur_x, init_y - cur_y
                            self.vertices = translate_points_based_on_mouse_movement_(deltaX=dx_t, deltaY=dy_t, points=self.vertices)
                            init_x, init_y = cur_x, cur_y

                else:
                    print("Rotation allowed ")
                    # Mouse motion event for rotation
                    if event.type == pygame.MOUSEMOTION and init_x is not None:
                        cur_x, cur_y = event.pos
                        dx, dy = cur_x - init_x, cur_y - init_y
                        self.vertices = rotate_points_based_on_mouse_movement_(dx, dy, points=self.vertices)
                        init_x, init_y = cur_x, cur_y

                # Mouse button up event
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    init_x, init_y = None, None

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_cube()
            pygame.display.flip()
            pygame.time.wait(10)

if __name__ == "__main__":
    play = PlayCube()
    play.play()
