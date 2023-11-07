import pygame
from pygame.locals import *
from pygame import *
from OpenGL.GL import *
from OpenGL.GLU import *

# CUBE

vertices = (
    (-1, -1, 1),  # 0
    (-1, -1, -1),  # 1
    (1, -1, -1),  # 2
    (1, -1, 1),  # 3
    (-1, 1, 1),  # 4
    (-1, 1, -1),  # 5
    (1, 1, -1),  # 6
    (1, 1, 1)  # 7
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 7),
    (5, 6),
    (6, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (0, 3, 7, 4),
    (4, 5, 6, 7)
)

# colors = (
#     (0.08, 0.02, 0.52),
#     (0.35, 0.04, 0.58),
#     (0.78, 0.16, 0.53),
#     (1, 1, 1)
# )

colors = (
    (0.5, 0.5, 0.5),
    (0.5, 0.5, 0.5),
    (0.5, 0.5, 0.5),
    (0.5, 0.5, 0.5)
)

# GROUND

ground_vertices = (
    (-4, -11, 2),  # 0
    (-4, -11, -2),  # 1
    (26, -11, -2),  # 2
    (26, -11, 2),  # 3
    (-4, -10, 2),  # 4
    (-4, -10, -2),  # 5
    (26, -10, -2),  # 6
    (26, -10, 2)  # 7
)

ground_edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 7),
    (5, 6),
    (6, 7)
)

ground_surfaces = (
    (0, 4, 2, 3),
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (0, 3, 7, 4),
    (4, 5, 6, 7)
)

gravity = 0.02

# parametry cube
c_position = [0, 0, 0]
velocity = 0.0


def cube():
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth(1)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((1, 1, 1))
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    for surface in surfaces:
        for i, vertex in enumerate(surface):
            glColor3fv(colors[i])
            glVertex3fv(vertices[vertex])
    glEnd()


def ground():
    # glEnable(GL_TEXTURE_2D)
    # glBindTexture(GL_TEXTURE_2D, glGenTextures(1))

    glBegin(GL_LINES)
    for edge in ground_edges:
        for vertex in edge:
            glColor3fv((1, 1, 1))
            glVertex3fv(ground_vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    for ground_surface in ground_surfaces:
        for i, vertex in enumerate(ground_surface):
            glColor3fv((0.15, 0.15, 0.15))
            glVertex3fv(ground_vertices[vertex])
    glEnd()


def main():
    global velocity
    global c_position
    pygame.init()

    display = (1152, 704)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    pygame.display.set_caption('Kacper Malinowski')
    font = pygame.font.SysFont('arial', 32)

    gluPerspective(42, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-11.0, 5, -27)  # początkowa pozycja
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)

    is_moving_right = False
    is_moving_left = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = 0.6
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    is_moving_right = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    is_moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    is_moving_right = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    is_moving_left = False

        if is_moving_right:
            c_position[0] += 0.2

        if is_moving_left:
            c_position[0] -= 0.2

        c_position[1] += velocity  # zmiana pozycji y
        velocity -= gravity

        if c_position[1] < -9:
            c_position[1] = -9
            velocity *= -0.2

        glClearColor(0.3, 0.3, 0.3, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslatef(c_position[0], c_position[1], 0.0)

        cube()
        glTranslatef(-c_position[0], -c_position[1], 0.0)

        # pisanie po ekranie test

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        textSurface = font.render("test", True, (95, 95, 255, 255)).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(50, 650)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

        # koniec pisania

        glTranslatef(0.0, 0.0, 0.0)
        ground()

        pygame.time.wait(10)
        pygame.display.flip()


main()