import cv2
import gpiozero
from face_detection_harcass import *
import time 

#Constant Variables
IMAGE_WIDTH = 50
IMAGE_HEIGHT = 50
CENTER_IMAGE_X = IMAGE_WIDTH / 2
CENTER_IMAGE_Y = IMAGE_HEIGHT / 2
FORWARD_SPEED = 1
TURING_SPEED = 1
RECTANGLE_SCALE = 0.5
#Recording size
size = (IMAGE_WIDTH, IMAGE_HEIGHT)

#Initializing
robot = gpiozero.Robot(right=(17,18), left=(4,14))
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
detect_face = FaceTracker()
#For saving the recording 
result = cv2.VideoWriter('test1.avi',cv2.VideoWriter_fourcc(*'XVID'), 15, size )
def robot_movement(object_position):
    """Moves the robot according to the object detected
        #object_postion: As a list"""
    if object_position:
        # if (object_position[0] > MIN_AREA) and (object_position[0] < MAX_AREA):
        if (object_position[0] + (object_position[2]/2)) > (CENTER_IMAGE_X + (IMAGE_WIDTH/4)):
            robot.left(TURING_SPEED)
            print("Turning right!")
        elif object_position[0] + (object_position[2]/2) < (CENTER_IMAGE_X - (IMAGE_WIDTH/4)):
            robot.right(TURING_SPEED)
            print("Turning left!")
        else:
            robot.forward(FORWARD_SPEED)
            print("Moving Forward!")
    else:
        robot.left(TURING_SPEED)
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
        result.write(frame)
        cv2.imshow("Robot Eye", frame)
        robot_movement(face_property)
        if cv2.waitKey(1) == 27:
            break
camera.release()
result.release()
cv2.destroyAllWindows()

