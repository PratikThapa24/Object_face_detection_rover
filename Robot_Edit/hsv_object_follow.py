import cv2
import numpy as np
import gpiozero

#Constant Variables
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
CENTER_IMAGE_X = IMAGE_WIDTH / 2
CENTER_IMAGE_Y = IMAGE_HEIGHT / 2
MIN_AREA = 300
MAX_AREA = 100000
FORWARD_SPEED = 1
TURING_SPEED = 1
HSV_VALUE = 28
lower_color =np.array([160, 100, 20])
higher_color =np.array([179, 255, 255])
size = (IMAGE_WIDTH, IMAGE_HEIGHT)
#Initializing
robot = gpiozero.Robot(left=(17, 18), right=(4, 14) )
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
#For saving the recording
result = cv2.VideoWriter('contour_test.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, size)
def robot_movement(object_position):
    """Moves the robot according to the object detected
        #object_postion: As a list"""
    if object_position:
        if (object_position[0] > MIN_AREA) and (object_position[0] < MAX_AREA):
            if object_position[1] > (CENTER_IMAGE_X + (IMAGE_WIDTH/3)):
                robot.right(TURING_SPEED)
                print("Turning right!")
            elif object_position[1] < (CENTER_IMAGE_X - (IMAGE_WIDTH/3)):
                robot.left(TURING_SPEED)
                print("Turning left!")
            else:
                robot.forward(FORWARD_SPEED)
                print("Moving Forward!")
        elif (object_position[0] < MIN_AREA):
            robot.left(TURING_SPEED)
            print("Target isn't larger enough, Searching!")
        else:
            robot.stop()
            print("Target not Found, Stopping!")
    else:
        robot.left(TURING_SPEED)
        print("Target not Found, searching")

def ball_property(contours):
    object_area = 0
    object_x = 0
    object_y = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        found_area = w*h
        center_x = x+(w/2)
        center_y = y+(h/2)
        if object_area < found_area:
            object_area = found_area
            object_x = center_x
            object_y = center_y
    if object_area > 0:
        ball_property = [object_area, object_x, object_y, x, y, w, h]
        return ball_property
    else:
        return None

while True:
    res, frame = camera.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Turns BGR->HSV
    color_mask = cv2.inRange(hsv, lower_color, higher_color) #Only keeps the color from the color range

    #Looking for contour
    contour, hierachy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    object_property = ball_property(contour)
    robot_movement(object_property)
    if object_property is not None:
        frame = cv2.rectangle(frame, (object_property[3], object_property[4]), (object_property[3]+object_property[5], object_property[4]+object_property[6]), (0,0,255),2 )
    #Shows the image in the screen
    result.write(frame)
    cv2.imshow("Robot Eye", frame)
    
    if cv2.waitKey(1) == 27:
        break

camera.release()
result.release()
cv2.destroyAllWindows()

