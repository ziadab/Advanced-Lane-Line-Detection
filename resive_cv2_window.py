import cv2
cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
im = cv2.imread("earth.jpg")                        # Read image
imS = cv2.resize(im, (960, 540))                    # Resize image
cv2.imshow("output", imS)                            # Show image
cv2.waitKey(0)                                      # Display the image infinitely until any keypress