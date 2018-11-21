from linefilter import LineFilter
from scipy.misc import imresize
from birdseye import Birdseye
from curves import Curves
from utils import roi
import numpy as np
import pickle
import time
import cv2

all_data = pickle.load(open("all_data.pkl","rb"))
# print(all_data)
camera_matrix = all_data["camera_matrix"]
dest_coef = all_data["distortion_coefficient"]

source_points = all_data["source_points"]
dest_points = all_data["dest_points"]
p = all_data["p"]

birdEye = Birdseye(source_points, dest_points, camera_matrix, dest_coef)
lineFilter = LineFilter(p)
curves = Curves(number_of_windows = 9,margin = 100, minimum_pixels = 50,ym_per_pix = 30 / 720 ,xm_per_pix = 3.7 / 700)

def debug_pipline(img):
    ground_img = birdEye.undistort(img)
    sky_view = birdEye.sky_view(img)

    binary_img = lineFilter.apply(ground_img)
    sobel_img = birdEye.sky_view(lineFilter.sobel_breakdown(ground_img))
    color_img = birdEye.sky_view(lineFilter.color_breakdown(ground_img))

    wb = np.logical_and(birdEye.sky_view(binary_img), roi(binary_img)).astype(np.uint8)
    result = curves.fit(wb)

    left_curve =  result['pixel_left_best_fit_curve']
    right_curve =  result['pixel_right_best_fit_curve']

    left_radius =  result['left_radius']
    right_radius =  result['right_radius']
    position = result['vehicle_position_words']
    curve_debug_img = result['image']

    processed_img = birdEye.project(ground_img, binary_img, left_curve, right_curve)
    # ground_img = undistort image 
    # binary_img = 

    return sky_view, sobel_img, color_img, curve_debug_img, processed_img, left_radius, right_radius, position
    #return sky_view, sobel_img, color_img, curve_debug_img, left_radius, right_radius, position

def visual_display(img):
    sky_view, sobel_img, color_img, curve_debug_img, processed_img, left_radius, right_radius, position = debug_pipline(img)
    # sky_view, sobel_img, color_img, curve_debug_img, left_radius, right_radius, position = debug_pipline(img)

    sky_view = imresize(sky_view, 0.25)
    sobel_img = imresize(sobel_img, 0.25)
    color_img = imresize(color_img, 0.25)
    curve_debug_img = imresize(curve_debug_img, 0.25)

    offset = [0, 320, 640, 960]
    width, height = 320,180

    processed_img[:height, offset[0]: offset[0] + width] = sky_view
    processed_img[:height, offset[1]: offset[1] + width] = sobel_img
    processed_img[:height, offset[2]: offset[2] + width] = color_img
    processed_img[:height, offset[3]: offset[3] + width] = curve_debug_img

    text_pos = "vehicle pos: " + position
    text_l = "left r: " + str(np.round(left_radius, 2))
    text_r = " right r: " + str(np.round(right_radius, 2))

    cv2.putText(processed_img, text_l, (20, 220), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(processed_img, text_r, (250, 220), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(processed_img, text_pos, (620, 220), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    # cv2.putText(processed_img, text_l, (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(processed_img, text_r, (250, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    # cv2.putText(processed_img, text_pos, (620, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    return processed_img
    #return sobel_img


cv2.namedWindow("visual display", cv2.WINDOW_NORMAL) 
cap = cv2.VideoCapture("videos\\project_video.mp4")

last_time = time.time()

while True:

    ret, fram = cap.read()
    gray = cv2.resize(visual_display(fram), (960, 540))
    print("Take {} seconds".format(time.time() - last_time))
    last_time = time.time()
    print("")
    cv2.imshow("visual display", gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
