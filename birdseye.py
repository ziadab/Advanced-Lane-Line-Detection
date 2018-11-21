from utils import show_dotted_image_using_cv2
import numpy as np
import cv2

class Birdseye(object):
    def __init__(self,source_points, dest_points, calibration_matrix, distortion_coefficient):
        self.spoints = source_points
        self.dpoints = dest_points
        self.src_point = np.array(source_points, np.float32)
        self.dest_points = np.array(dest_points, np.float32)
        self.camera_matrix = calibration_matrix
        self.dist_coef = distortion_coefficient

        self.warp_matrix = cv2.getPerspectiveTransform(self.src_point, self.dest_points)
        self.inv_warp_matrix = cv2.getPerspectiveTransform(self.dest_points, self.src_point)

    def undistort(self, image, show_dotted = False):
        image = cv2.undistort(image, self.camera_matrix, self.dist_coef, None, self.camera_matrix)

        if show_dotted:
          show_dotted_image_using_cv2(image, self.spoints)

        return image

    def sky_view(self, ground_image, show_dotted = False):
        image = self.undistort(ground_image)
        shape = (image.shape[1], image.shape[0])
        wrap_image = cv2.warpPerspective(image, self.warp_matrix, shape, flags = cv2.INTER_LINEAR)
        if show_dotted:
            show_dotted_image_using_cv2(wrap_image, self.dpoints)
        return wrap_image

    def project(self, ground_image, sky_lane, left_fit, right_fit, color = (0, 255, 0)):

      z = np.zeros_like(sky_lane)
      sky_lane = np.dstack((z, z, z))

      kl, kr = left_fit, right_fit
      h = sky_lane.shape[0]
      ys = np.linspace(0, h - 1, h)
      lxs = kl[0] * (ys**2) + kl[1]* ys +  kl[2]
      rxs = kr[0] * (ys**2) + kr[1]* ys +  kr[2]

      pts_left = np.array([np.transpose(np.vstack([lxs, ys]))])
      pts_right = np.array([np.flipud(np.transpose(np.vstack([rxs, ys])))])
      pts = np.hstack((pts_left, pts_right))

      cv2.fillPoly(sky_lane, np.int_(pts), color)

      shape = (sky_lane.shape[1], sky_lane.shape[0])
      ground_lane = cv2.warpPerspective(sky_lane, self.inv_warp_matrix, shape)

      result = cv2.addWeighted(ground_image, 1, ground_lane, 0.3, 0)
      return result
