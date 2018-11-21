import cv2
import numpy as np
#from PIL import Image

class Chessboard(object):
	def __init__(self,path,nx = 9, ny=6):
		self.path = path
		self.nx, self.ny = nx, ny
		# Surface of work
		self.n = (self.nx, self.ny)

		# Read the image and cvt to gray scale
		image = cv2.imread(self.path)
		gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

		self.rows, self.cols, self.channels = image.shape
		self.dimensions = (self.rows, self.cols)

		self.has_corners, self.corners = cv2.findChessboardCorners(gray, self.n, None)
		self.object_points = self.get_object_points()
		self.matrix, self.distortion, self.can_undistort = None, None, False

	def get_object_points(self):
		number_of_points = self.nx * self.ny
		points = np.zeros((number_of_points, 3),np.float32)
		points[:, :2] = np.mgrid[0:self.nx, 0:self.ny].T.reshape(-1, 2)
		return points

	def image(self):
		return cv2.imread(self.path)

	def image_with_corners(self):
		img = self.image()
		if self.has_corners:
			cv2.drawChessboardCorners(img, self.n, self.corners, self.has_corners)
		return img

	def undistorted_image(self):
		temp_image = None
		if self.can_undistort:
		  temp_image = cv2.imread(self.path)
		  temp_image = cv2.undistort(temp_image, self.matrix, self.distortion, None, self.matrix)
		return temp_image

	def load_undistort_params(self, distortion, camera_matrix):
			self.distortion = distortion
			self.matrix = camera_matrix
			self.can_undistort = True
