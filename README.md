# Object_face_detection_rover
Autonomous Face and Object Detection Rover

Welcome to the GitHub repository of my exciting project - an Autonomous Face and Object Detection Rover! This project showcases my passion for computer vision, deep learning, and building intelligent systems using Python.
How it Works:

Hardware Assembly: I started by assembling the required components, including a Raspberry Pi 3B+ (the brain), a camera, chassis, motors, wires, breadboards, and more. Understanding the electronics and current flow was essential, and I found helpful information in the GPIOZero documentation.

Computer Vision Fundamentals: To delve into computer vision and deep learning, I studied relevant books and took a course on Udemy. This knowledge became the foundation for training my models.

Face Detection: I initially attempted training a Convolutional Neural Network (CNN) for face detection. However, due to limited data, I opted for the Haarcascade algorithm, utilizing a pre-trained model. This proved successful in identifying faces.

Face Tracking: The DetectionCSRT algorithm was employed to track the detected face effectively. The rover continuously follows the face within the frame, creating an engaging visual experience.

Integration with Motors: To bring the rover to life, I integrated the face detection with motor control. I drew a rectangle around the face, and the rover's movement was determined based on the position of the rectangle. For instance, if the face was at a quarter of the screen, the rover would turn right, and vice versa.

Future Enhancements:

This project has endless possibilities for growth and expansion. Given more resources, I plan to add features like:

Obstacle Detection: Integrating servo motors with an HC-SR04 ultrasonic sensor to detect nearby objects and enabling the rover to stop or change direction accordingly.

Autonomous Navigation: Integrating a LIDAR system to allow the rover to learn autonomously and navigate its path, making it more self-sufficient.

3D Printing: Exploring 3D printing techniques to enhance the rover's appearance and functionalities.

Conclusion:

Creating this Autonomous Face and Object Detection Rover has been an immensely rewarding experience. It allowed me to explore the realms of hardware, electrical engineering, and software development while learning and implementing exciting computer vision concepts.
![IMG_6750](https://github.com/PratikThapa24/Object_face_detection_rover/assets/125596457/26bc177e-9849-42a0-9996-19b7bc2d1466)

