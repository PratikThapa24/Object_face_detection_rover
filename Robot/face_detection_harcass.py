import cv2
class FaceTraceker:
    def __init__(self):
        self.tracker = cv2.TrackerCSRT_create()
        self.face_detected = False
        self.track_window = None
        self.roi_hist = None

    def track_face(self, frame):
    # Read frame from the video capture
    # Detect faces in the frame
        if not self.face_detected:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            face_rects = face_cascade.detectMultiScale(frame)

            if len(face_rects) > 0:
                (face_x, face_y, w, h) = tuple(face_rects[0])
                self.track_window = (face_x, face_y, w, h)

                # Initialize the tracker
                self.tracker.init(frame, self.track_window)

                # Extract ROI for histogram calculation
                roi = frame[face_y:face_y + h, face_x:face_x + w]
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                self.roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
                cv2.normalize(self.roi_hist, self.roi_hist, 0, 255, cv2.NORM_MINMAX)

                self.face_detected = True

        else:
            # Convert frame to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Calculate back projection
            dst = cv2.calcBackProject([hsv], [0], self.roi_hist, [0, 180], 1)

            # Update the tracker
            ret, self.track_window = self.tracker.update(frame)

            # Draw the bounding box
            if ret:
                x, y, w, h = tuple(map(int, self.track_window))
                face_dimension = (x, y, w, h)
                return face_dimension

# detect_face = FaceTraceker()
# #Initializing the class
# while True:
#     res, frame = camera.read()
#     if res:
#         face_property = detect_face.track_face(frame)
#         if face_property is not None:
#             frame = cv2.rectangle(frame, (face_property[0], face_property[1]), (face_property[0] + face_property[2], face_property[1] + face_property[3]), (0, 0, 255), 2)
#         cv2.imshow("Robo", frame)
#         if cv2.waitKey(1) == 27:
#             break
#
# camera.release()
# cv2.destroyAllWindows()
