#from matplotlib.patches import Circle
#import matplotlib.pyplot as plt
import numpy as np
import cv2

def show_dotted_image_using_cv2(image, points, thickness = 4, color = [255,0,255], d =15):

    cv2.line(image, points[0], points[1], color, thickness)
    cv2.line(image, points[2], points[3], color, thickness)

    for (x, y) in points:
        cv2.circle(image, (x, y), d, color, thickness)

def show_dotted_image_using_plt(image, points, thickness = 4, color = [255,0,255], d =15):

    cv2.line(image, points[0], points[1], color, thickness)
    cv2.line(image, points[2], points[3], color, thickness)

    #fig, ax = plt.subplots(1)
    #ax.set_aspect('equal')
    #ax.imshow(image)

    #for (x, y) in points:
    #    dots = Circle((x, y), d)
    #    ax.add_patch(dots)

    #plt.show()

def scale_abs(x, m = 255):
  x = np.absolute(x)
  x = np.uint8(m * x / np.max(x))
  return x

def roi(gray, mn = 125, mx = 1200):
  m = np.copy(gray) + 1
  m[:, :mn] = 0
  m[:, mx:] = 0
  return m
