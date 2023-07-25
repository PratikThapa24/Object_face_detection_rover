import cv2

class FaceTracker:
    def __init__(self):
        self.tracker = cv2.TrackerCSRT_create()
        self.face_detected = False
        self.track_window = None
        self.roi_hist = None
        self.frames_since_detection = 0
        self.max_frames_to_detect = 30

    def track_face(self, frame):
        if not self.face_detected or self.frames_since_detection >= self.max_frames_to_detect:
            face_cascade = cv2.CascadeClassifier('cups.xml')
            face_rects = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

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
                self.frames_since_detection = 0

        else:
            # Convert frame to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Calculate back projection
            dst = cv2.calcBackProject([hsv], [0], self.roi_hist, [0, 180], 1)

            # Update the tracker
            ret, self.track_window = self.tracker.update(frame)

            if ret:
                x, y, w, h = tuple(map(int, self.track_window))
                face_dimension = (x, y, w, h)
                self.frames_since_detection = 0
                return face_dimension
            else:
                self.face_detected = False
                self.frames_since_detection += 1

        self.frames_since_detection += 1

