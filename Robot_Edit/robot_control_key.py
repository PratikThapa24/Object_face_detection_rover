#Import
import gpiozero
import pygame
from pygame.locals import *
import cv2

#Slow decay

#Initializing & object library
pygame.init()
robot = gpiozero.Robot(left=(17,18), right=(4, 14))
cap = cv2.VideoCapture(0)
cv2.namedWindow("Robot_camera")

#Constants
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
speed = 1

#Initializing the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robot Control Rasp")

#Class for the Button
class Button:
    def __init__(self, width, height, color, hover_color, text, text_color):
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.is_pressed = False

    def draw(self, x, y):
        rect = pygame.Rect(x, y, self.width, self.height)
        if self.is_pressed:
            pygame.draw.rect(screen, self.hover_color, rect)
        else:
            pygame.draw.rect(screen, self.color, rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event, pressed_key):
        if event.type == KEYDOWN:
            if event.key == pressed_key:
                self.is_pressed = True

        elif event.type == KEYUP:
            if event.key == pressed_key:
                self.is_pressed = False

class Robot_dir:
    def __init__(self):
        self.forward = False
        self.backward = False
        self.right = False
        self.left = False
    def check_key_pressed(self,event):
        if event.type == KEYDOWN:
            if event.key == K_w:
                self.forward = True
            elif event.key == K_s:
                self.backward = True
            elif event.key == K_d:
                self.right = True
            elif event.key == K_a:
                self.left = True
        elif event.type == KEYUP:
            self.forward = False
            self.backward = False
            self.right = False
            self.left = False

    def move_robot(self):
        if self.forward:
            print("Moving Forward")
            robot.forward(speed)
        elif self.backward:
            print("Moving Backward")
            robot.backward(speed)
        elif self.right:
            print("Turning Right")
            robot.right(speed)
        elif self.left:
            print("Turning Left")
            robot.left(speed)
        else:
            # print("Robot Stopped")
            robot.stop()


button_width, button_height = 80, 80
color = (255, 0, 0)  # Button color
hover_color = (0, 255, 0)  # Color when button is pressed
text_color = (255, 255, 255)  # Text color

#Classes
key_W = Button(button_width, button_height, color, hover_color, 'W', text_color)
key_A = Button(button_width, button_height, color, hover_color, 'A', text_color)
key_D = Button(button_width, button_height, color, hover_color, 'D', text_color)
key_S = Button(button_width, button_height, color, hover_color, 'S', text_color)
robot_body = Robot_dir()

running = True
while running:
    ret, frame = cap.read()
    cv2.imshow("Robot_camera", frame)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        #Check the event
        key_W.handle_event(event, K_w)
        key_A.handle_event(event, K_a)
        key_D.handle_event(event, K_d)
        key_S.handle_event(event, K_s)
        robot_body.check_key_pressed(event)

    #Camera if condition to close
    if cv2.waitKey(1) == 27:
        break
    robot_body.move_robot()
    screen.fill((0, 0, 0))
    key_W.draw(80, 20)
    key_A.draw(20, 80)
    key_D.draw(140, 80)
    key_S.draw(80, 140)
    pygame.display.flip()

pygame.quit()
cap.release()
cv2.destroyAllWindows()
