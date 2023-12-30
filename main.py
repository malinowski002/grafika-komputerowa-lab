from time import sleep as wait
from math import cos, sin

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

colors = (
    (0.5, 0.5, 0.5),
    (0.5, 0.5, 0.5),
    (0.5, 0.5, 0.5),
    (0.5, 0.5, 0.5)
)

# GROUND

ground_vertices = (
    (0, -11, 2),  # 0
    (0, -11, -2),  # 1
    (22, -11, -2),  # 2
    (22, -11, 2),  # 3
    (0, -10, 2),  # 4
    (0, -10, -2),  # 5
    (22, -10, -2),  # 6
    (22, -10, 2)  # 7
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

is_game_on = True
enemies_survived = 0
gravity = 0.03
is_jumping = True
on_ground = False
player_score = 0
player_lives = 3

# parametry cube
c_position = [2, 0, 0]
velocity = 0.0

# źródło światła punktowego
light_position = [10.0, 10.0, 10.0, 1.0]


def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))  # Kolor światła rozproszonego
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))  # Kolor światła odbitego
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))  # Kolor światła otoczenia


def cube():
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth(1)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0.37, 0.37, 1))
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    for surface in surfaces:
        glNormal3fv(calculate_surface_normal(surface))  # Dodane obliczanie wektora normalnego dla oświetlenia
        for i, vertex in enumerate(surface):
            glColor3fv((0.47, 0.47, 1))
            glVertex3fv(vertices[vertex])
    glEnd()


def ground():
    glBegin(GL_LINES)
    for edge in ground_edges:
        for vertex in edge:
            glColor3fv((0.27, 0.58, 0.17))
            glVertex3fv(ground_vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    for ground_surface in ground_surfaces:
        glNormal3fv(calculate_surface_normal(ground_surface))  # Dodane obliczanie wektora normalnego dla oświetlenia
        for i, vertex in enumerate(ground_surface):
            glColor3fv((0.38, 0.78, 0.22))
            glVertex3fv(ground_vertices[vertex])
    glEnd()


enemy_position = [15, -9, 0]


def enemy():
    glEnable(GL_BLEND)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth(1)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0.75, 0, 0))
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    for surface in surfaces:
        glNormal3fv(calculate_surface_normal(surface))  # Dodane obliczanie wektora normalnego dla oświetlenia
        for i, vertex in enumerate(surface):
            glColor3fv((1, 0.2, 0.2))
            glVertex3fv(vertices[vertex])
    glEnd()


def calculate_surface_normal(surface):
    # Funkcja do obliczania wektora normalnego dla podanej powierzchni
    v1 = vertices[surface[0]]
    v2 = vertices[surface[1]]
    v3 = vertices[surface[2]]
    normal = [
        (v2[1] - v1[1]) * (v3[2] - v1[2]) - (v2[2] - v1[2]) * (v3[1] - v1[1]),
        (v2[2] - v1[2]) * (v3[0] - v1[0]) - (v2[0] - v1[0]) * (v3[2] - v1[2]),
        (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
    ]
    length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
    return [value / length for value in normal]


def check_collision():
    global player_lives
    global is_game_on
    if (c_position[0] - enemy_position[0]) ** 2 < 2 and \
            (c_position[1] - enemy_position[1]) ** 2 < 2 and \
            (c_position[2] - enemy_position[2]) ** 2 < 2:
        print("Collided with the enemy")
        if player_lives > 1:
            player_lives -= 1
        else:
            player_lives -= 1
            wait(3)
            is_game_on = False
            print("You lost")
        enemy_position[0] = 30


def main():
    global enemies_survived
    global is_game_on
    global player_score
    global player_lives
    global velocity
    global c_position
    global enemy_position
    global is_jumping
    global on_ground
    pygame.init()

    display = (1152, 704)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    pygame.display.set_caption('Kacper Malinowski')
    font = pygame.font.SysFont('arial', 32)

    gluPerspective(32, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-11.0, 6, -27)  # początkowa pozycja
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)

    is_moving_right = False
    is_moving_left = False

    angle = 0.0

    while is_game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = 0.6
                    is_jumping = True
                    on_ground = False
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

        # zmiana pozycji y cube

        if is_jumping:
            c_position[1] += velocity
            velocity -= gravity

            if c_position[1] < -9:
                c_position[1] = -9
                velocity = 0
                is_jumping = False
                on_ground = True

        # pozycja enemy

        if enemy_position[0] < -4:
            enemies_survived += 1
            player_score = enemies_survived
            enemy_position[0] = 25
        else:
            enemy_position[0] -= (0.1 + enemies_survived*0.05)

        glClearColor(0.85, 0.94, 0.95, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # sprawdzanie kolizji

        check_collision()

        # rysowanie cube

        glTranslatef(c_position[0], c_position[1], 0.0)
        cube()
        glTranslatef(-c_position[0], -c_position[1], 0.0)

        # enemy
        glTranslatef(enemy_position[0], enemy_position[1], enemy_position[2])
        enemy()
        glTranslatef(-enemy_position[0], -enemy_position[1], -enemy_position[2])

        # pisanie po ekranie test

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        textSurface = font.render(f"Score: {player_score}", True, (95, 95, 255, 255)).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(50, 650)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

        textSurface = font.render(f"Lives: {player_lives}", True, (255, 95, 95, 255)).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(50, 600)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

        # koniec pisania

        radius = 10.0
        light_position[0] = radius * cos(angle)
        light_position[1] = radius * sin(angle)
        light_position[2] = 5.0

        setup_lighting()
        angle += 0.03

        glTranslatef(0.0, 0.0, 0.0)
        ground()

        pygame.display.flip()

        pygame.time.wait(10)


main()
