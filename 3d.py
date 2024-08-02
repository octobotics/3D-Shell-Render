from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import time

x_rotation = 0.0
y_rotation = 0.0
last_x = 0
last_y = 0
is_dragging = False
zoom = -15.0  
t = 0.0  
start_time = time.time()

def calculate_vertical_lines(diameter, height):
    base_lines = 6
    aspect_ratio = height / diameter
    return int(base_lines * aspect_ratio)

def calculate_horizontal_lines(diameter, height):
    return calculate_vertical_lines(diameter, height)

def draw_rectangle_as_cylinder(diameter, height):
    breadth = diameter
    length = height
    radius = diameter / 2.0
    half_height = height / 2.0

    glColor4f(0.0, 0.0, 0.3, 0.5)

    if t < 1.0:
        
        glBegin(GL_QUADS)
        glVertex3f(-breadth / 2, -length / 2, 0)
        glVertex3f(breadth / 2, -length / 2, 0)
        glVertex3f(breadth / 2, length / 2, 0)
        glVertex3f(-breadth / 2, length / 2, 0)
        glEnd()

        glColor4f(1.0, 1.0, 1.0, 1.0)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-breadth / 2, -length / 2, 0)
        glVertex3f(breadth / 2, -length / 2, 0)
        glVertex3f(breadth / 2, length / 2, 0)
        glVertex3f(-breadth / 2, length / 2, 0)
        glEnd()
    else:
        
        slices = 256
        glBegin(GL_QUAD_STRIP)
        for i in range(slices + 1):
            angle = 2.0 * np.pi * i / slices
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            glVertex3f(x, y, -half_height)
            glVertex3f(x, y, half_height)
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, half_height)
        for i in range(slices + 1):
            angle = 2.0 * np.pi * i / slices
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            glVertex3f(x, y, half_height)
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, -half_height)
        for i in range(slices + 1):
            angle = 2.0 * np.pi * i / slices
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            glVertex3f(x, y, -half_height)
        glEnd()

        glColor4f(1.0, 1.0, 1.0, 1.0)
        glLineWidth(2.0)

        for i in range(calculate_vertical_lines(diameter, height)):
            angle = 2.0 * np.pi * i / calculate_vertical_lines(diameter, height)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            glBegin(GL_LINES)
            glVertex3f(x, y, -half_height)
            glVertex3f(x, y, half_height)
            glEnd()

        glBegin(GL_LINE_LOOP)
        for i in range(slices + 1):
            angle = 2.0 * np.pi * i / slices
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            glVertex3f(x, y, half_height)
        glEnd()

        glBegin(GL_LINE_LOOP)
        for i in range(slices + 1):
            angle = 2.0 * np.pi * i / slices
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            glVertex3f(x, y, -half_height)
        glEnd()

        for i in range(1, calculate_horizontal_lines(diameter, height) + 1):
            z = -half_height + (i * height / (calculate_horizontal_lines(diameter, height) + 1))
            glBegin(GL_LINE_LOOP)
            for j in range(slices + 1):
                angle = 2.0 * np.pi * j / slices
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                glVertex3f(x, y, z)
            glEnd()

def display():
    global x_rotation, y_rotation, zoom
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, zoom)
    glRotatef(x_rotation, 1.0, 0.0, 0.0)
    glRotatef(y_rotation, 0.0, 1.0, 0.0)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)

    draw_rectangle_as_cylinder(diameter, height)

    glDisable(GL_BLEND)
    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def mouse(button, state, x, y):
    global last_x, last_y, is_dragging
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            is_dragging = True
            last_x = x
            last_y = y
        elif state == GLUT_UP:
            is_dragging = False

def motion(x, y):
    global last_x, last_y, x_rotation, y_rotation
    if is_dragging:
        dx = x - last_x
        dy = y - last_y
        x_rotation += dy * 0.5
        y_rotation += dx * 0.5
        last_x = x
        last_y = y
        glutPostRedisplay()

def keyboard_special(key, x, y):
    global zoom
    if key == GLUT_KEY_UP:
        zoom += 0.1
    elif key == GLUT_KEY_DOWN:
        zoom -= 0.1
    glutPostRedisplay()

def update_animation(value):
    global t, start_time
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > 5.0: 
        t += 0.01
        if t > 1.0:
            t = 1.0
    glutPostRedisplay()
    glutTimerFunc(16, update_animation, 0)

def main(diameter, height):
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"KEK")
    glEnable(GL_DEPTH_TEST)

    glClearColor(0.0, 0.0, 0.3, 1.0)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutSpecialFunc(keyboard_special)  
    glutTimerFunc(16, update_animation, 0)  
    glutMainLoop()

if __name__ == "__main__":
    diameter = 2.0
    height = 4.0
    main(diameter, height)

