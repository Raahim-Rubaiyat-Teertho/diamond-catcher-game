from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

score = 0
color_end = False
catcher_move = True

class Catcher:
    def __init__(self, position, length, height):
        self.position = position
        self.length = length
        self.height = height
        

    def draw(self):

        glBegin(GL_LINES)
        glVertex2f(self.position+10, 0)
        glVertex2f(self.position + self.length, 0)

        glVertex2f(self.position, self.height)
        glVertex2f(self.position + self.length+10, self.height)

        glVertex2f(self.position + 10, 0)
        glVertex2f(self.position, self.height)

        glVertex2f(self.position + self.length, 0)
        glVertex2f(self.position + self.length + 10, self.height)
        glEnd()

class Diamond:
    def __init__(self, position, size=8, speed=3):
        self.position = position
        self.size = size
        self.speed = speed
        self.active = True

    def draw(self):
        if self.active:
            glBegin(GL_LINES)
            glVertex2f(self.position[0], self.position[1] + self.size)
            glVertex2f(self.position[0] + self.size, self.position[1])

            glVertex2f(self.position[0] + self.size, self.position[1])
            glVertex2f(self.position[0], self.position[1] - self.size)

            glVertex2f(self.position[0], self.position[1] - self.size)
            glVertex2f(self.position[0] - self.size, self.position[1])

            glVertex2f(self.position[0] - self.size, self.position[1])
            glVertex2f(self.position[0], self.position[1] + self.size)
            glEnd()


def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if(abs(dx) >= abs(dy)):
        if(dx > 0 and dy >0):
            pass

        elif(dx > 0 and dy <0):
            x1 = x1
            y1 = -y1
            x2 = x2
            y2 = -y2

        elif(dx < 0 and dy < 0):
            x1 = -x1
            y1 = -y1
            x2 = -x2
            y2 = -y2

        elif(dx < 0 and dy > 0):
            x1 = -x1
            y1 = y1
            x2 = -x2
            y2 = y2

    else:
        if(dx > 0 and dy > 0):
            x1 = y1
            y1 = x1
            x2 = y2
            y2 = x2

        elif(dx < 0 and dy > 0):
            x1 = -y1
            y1 = x1
            x2 = -y2
            y2 = x2

        elif(dx > 0 and dy > 0):
            x1 = -y1
            y1 = -x1
            x2 = -y2
            y2 = -x2

        elif(dx > 0 and dy < 0):
            x1 = y1
            y1 = -x1
            x2 = y2
            y2 = -x2


def draw_line(x1, y1, x2, y2):
    findZone(x1, y1, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    d = (2 * dy) - dx
    incE = (2 * dy)
    incNE = 2 * (dy - dx)
    y = y1
    x = x1
    while x <= x2:
        draw_points(x, y)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1


def iterate():
    glViewport(0, 0, 400, 550)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 400, 0.0, 550, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

diamonds = []

def showScreen():
    global color_end
    global diamonds
    global score

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(1, 1, 1)
    #restart button
    # draw_line(30, 500, 50, 500)
    # draw_line(30, 500, 40, 540)
    # draw_line(30, 500, 40, 480)

    if(color_end == False):
        glColor3f(1.0, 1.0, 1.0)

    else:
        glColor3f(1, 0, 0)


    if(Catcher.position < 10):
        Catcher.position = 0
    elif(Catcher.position + Catcher.length > 390):
        Catcher.position = 390 - Catcher.length

    Catcher.draw()

    glColor3f(1.0, 1.0, 0.0)
    for i in diamonds:
        i.draw()
        if i.active:
            i.position[1] -= i.speed

            if (Catcher.position <= i.position[0] <= Catcher.position + Catcher.length and 0 <= i.position[1] <= Catcher.height):
                diamonds.append(Diamond(position=[random.uniform(0, 400), 550])) 
                i.active = False
                score += 1
                print("Score:", score)
            
            elif(i.position[1] <= 0):
                print('Game Over')
                i.active = False
                color_end = True

    glutSwapBuffers()

def update(i):
    global color_end
    glutTimerFunc(16, update, 0)

    global diamonds

    glutPostRedisplay()

def special_keys(key, x, y):
    global color_end 

    if(color_end == False):
        if key == GLUT_KEY_LEFT:
            Catcher.position -= 10
        elif key == GLUT_KEY_RIGHT:
            Catcher.position += 10


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(400, 550)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(showScreen)
glutSpecialFunc(special_keys)
glutTimerFunc(0, update, 0)

Catcher = Catcher(position=150, length=70, height=10)
diamonds.append(Diamond(position=[random.uniform(0, 400), 550]))

glutMainLoop()
