from birdseye import Birdseye
import numpy as np
import pickle
import cv2

calibration_data = pickle.load(open("calibration_data.pkl","rb"))

camera_matrix = calibration_data['camera_matrix']
dist_coef = calibration_data['distortion_coefficient']

source_points = [(580, 460), (205, 720), (1110, 720), (703, 460)]
dest_points = [(320, 0), (320, 720), (960, 720), (960, 0)]

birdEye = Birdseye(source_points, dest_points, camera_matrix, dist_coef)

cap = cv2.VideoCapture("/home/zeus/Desktop/MyOwnLineDetection/videos/project_video.mp4")

cv2.namedWindow("undistort", cv2.WINDOW_NORMAL)
cv2.namedWindow("sky view", cv2.WINDOW_NORMAL)

while True:
    ret, img = cap.read()
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    undistort = birdEye.undistort(img, show_dotted=True)
    sky_view = birdEye.sky_view(img, show_dotted=True)
    undistort = cv2.resize(undistort, (800, 700))
    sky_view = cv2.resize(sky_view, (800, 700))
    # HLS MODE
    # cv2.imshow("undistort", cv2.cvtColor(undistort, cv2.COLOR_RGB2HLS))
    # cv2.imshow("sky view", cv2.cvtColor(sky_view, cv2.COLOR_RGB2HLS))
    cvZ.imshow("undistort", undistort)
    cv2.imshow("sky view",sky_view)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
