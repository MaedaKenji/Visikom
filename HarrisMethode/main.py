import cv2
import numpy
import os

# using os to get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
img = cv2.imread(os.path.join(current_directory, 'img.jpg'))
img = cv2.resize(img, (640, 480))

if img is None:
    print("Image not found")
    exit()

cv2.imshow('Original Image', img)    
#Smoothing with Ismooth = G(x,y,σ) * I(x,y)
sigma = 1
kernel_size = int(2 * (3 * sigma) + 1)
kernel = cv2.getGaussianKernel(kernel_size, sigma)
kernel = kernel @ kernel.T
smooth_img = cv2.filter2D(img, -1, kernel)
#Smoothing with Ismooth = G(x,y,σ) * I(x,y)
cv2.imshow('Smooth Image', smooth_img)

# Gradient calculation
gray_img = cv2.cvtColor(smooth_img, cv2.COLOR_BGR2GRAY)
gradient_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
gradient_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)

# Convert gradients to absolute values and scale to 8-bit
abs_gradient_x = cv2.convertScaleAbs(gradient_x)
abs_gradient_y = cv2.convertScaleAbs(gradient_y)

# Combine gradients
gradient_magnitude = cv2.addWeighted(abs_gradient_x, 0.5, abs_gradient_y, 0.5, 0)

cv2.imshow('Gradient Magnitude', gradient_magnitude)

# Compute the Harris matrix
# Compute products of derivatives
Ixx = gradient_x ** 2
Iyy = gradient_y ** 2
Ixy = gradient_x * gradient_y

# Apply Gaussian filter to the products
Ixx = cv2.GaussianBlur(Ixx, (kernel_size, kernel_size), sigma)
Iyy = cv2.GaussianBlur(Iyy, (kernel_size, kernel_size), sigma)
Ixy = cv2.GaussianBlur(Ixy, (kernel_size, kernel_size), sigma)

# Compute the Harris response matrix
k = 0.04  # Harris corner constant
det_M = (Ixx * Iyy) - (Ixy ** 2)
trace_M = Ixx + Iyy
harris_response = det_M - k * (trace_M ** 2)

# Normalize the Harris response for visualization
harris_response_normalized = cv2.normalize(harris_response, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
cv2.imshow('Harris Response', harris_response_normalized)

# Calculate angle response Harris
angle_response = numpy.arctan2(gradient_y, gradient_x)
angle_response_degrees = numpy.degrees(angle_response)
angle_response_normalized = cv2.normalize(angle_response_degrees, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

cv2.imshow('Angle Response', angle_response_normalized)

# Thresholding the Harris response
threshold = 0.1 * harris_response.max()
keypoints = numpy.argwhere(harris_response > threshold)

# Non maximum suppression
corners = []
for y, x in keypoints:
    if harris_response[y, x] == numpy.max(harris_response[y-1:y+2, x-1:x+2]):
        corners.append((x, y))

# Draw corners on the original image
for corner in corners:
    cv2.circle(img, corner, 5, (0, 0, 255), -1)

cv2.imshow('Corners', img)
if cv2.waitKey(0) & 0xFF == 27:
    cv2.destroyAllWindows()
    exit()
