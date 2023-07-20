import cv2
import gpiozero
from face_detection_harcass import *

#Constant Variables
IMAGE_WIDTH = 160
IMAGE_HEIGHT = 160
CENTER_IMAGE_X = IMAGE_WIDTH / 2
CENTER_IMAGE_Y = IMAGE_HEIGHT / 2
FORWARD_SPEED = 0.3
TURING_SPEED = 0.2
RECTANGLE_SCALE = 0.5

#Initializing
# robot = gpiozero.Robot()
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
detect_face = FaceTraceker()

def robot_movement(object_position):
    """Moves the robot according to the object detected
        #object_postion: As a list"""
    if object_position:
        # if (object_position[0] > MIN_AREA) and (object_position[0] < MAX_AREA):
        if (object_position[0] + (object_position[2]/2)) > (CENTER_IMAGE_X + (IMAGE_WIDTH/4)):
            # robot.right(TURING_SPEED)
            print("Turning right!")
        elif object_position[0] + (object_position[2]/2) < (CENTER_IMAGE_X - (IMAGE_WIDTH/4)):
            # robot.left(TURING_SPEED)
            print("Turning left!")
        else:
            # robot.forward(FORWARD_SPEED)
            print("Moving Forward!")
    else:
        # robot.left(TURING_SPEED)
        print("Object, not found turning left!")

while True:
    res, frame = camera.read()
    if res:
        frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
        face_property = detect_face.track_face(frame)
        if face_property is not None:
            face_width = int(face_property[2] * RECTANGLE_SCALE)
            face_height = int(face_property[3] * RECTANGLE_SCALE)
            face_x = int(face_property[0] + (face_property[2] - face_width) / 2)
            face_y = int(face_property[1] + (face_property[3] - face_height) / 2)
            frame = cv2.rectangle(frame, (face_x, face_y), (face_x + face_width, face_y + face_height), (0, 0, 255), 2)
        #Shows the image in the screen
        cv2.imshow("Robot Eye", frame)
        robot_movement(face_property)
        if cv2.waitKey(1) == 27:
            break

camera.release()
cv2.destroyAllWindows()

