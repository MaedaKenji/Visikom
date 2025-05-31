import os
import base64
import numpy as np
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({'error': 'Invalid image'}), 400
    
    # Resize image
    img = cv2.resize(img, (640, 480))
    original_img_copy = img.copy()
    
    # Convert to grayscale at the beginning to reduce noise in all stages
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian smoothing to reduce noise
    sigma = 1
    kernel_size = int(2 * (3 * sigma) + 1)
    smooth_img = cv2.GaussianBlur(gray_img, (kernel_size, kernel_size), sigma)
    
    # Calculate image gradients
    gradient_x = cv2.Sobel(smooth_img, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(smooth_img, cv2.CV_64F, 0, 1, ksize=3)
    
    abs_gradient_x = cv2.convertScaleAbs(gradient_x)
    abs_gradient_y = cv2.convertScaleAbs(gradient_y)
    gradient_magnitude = cv2.addWeighted(abs_gradient_x, 0.5, abs_gradient_y, 0.5, 0)
    
    # Harris corner detection
    Ixx = gradient_x ** 2
    Iyy = gradient_y ** 2
    Ixy = gradient_x * gradient_y
    
    # Apply Gaussian blur to the derivatives
    Ixx = cv2.GaussianBlur(Ixx, (kernel_size, kernel_size), sigma)
    Iyy = cv2.GaussianBlur(Iyy, (kernel_size, kernel_size), sigma)
    Ixy = cv2.GaussianBlur(Ixy, (kernel_size, kernel_size), sigma)
    
    k = 0.04  
    det_M = (Ixx * Iyy) - (Ixy ** 2)
    trace_M = Ixx + Iyy
    harris_response = det_M - k * (trace_M ** 2)
    
    harris_response_normalized = cv2.normalize(harris_response, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    angle_response = np.arctan2(gradient_y, gradient_x)
    angle_response_degrees = np.degrees(angle_response)
    angle_response_normalized = cv2.normalize(angle_response_degrees, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # Find Harris corners
    threshold = 0.1 * harris_response.max()
    keypoints = np.argwhere(harris_response > threshold)
    corners = []
    for y, x in keypoints:
        if harris_response[y, x] == np.max(harris_response[max(0, y-1):min(harris_response.shape[0], y+2), 
                                           max(0, x-1):min(harris_response.shape[1], x+2)]):
            corners.append((x, y))
    
    # Draw Harris corners on the original image
    harris_corners_img = original_img_copy.copy()
    for corner in corners:
        cv2.circle(harris_corners_img, corner, 5, (0, 0, 255), -1)  # Red circles
    
    # Good Features to Track (Shi-Tomasi)
    gftt_corners = cv2.goodFeaturesToTrack(
        smooth_img,
        maxCorners=1000,
        qualityLevel=0.01,
        minDistance=10,
        blockSize=3,
        useHarrisDetector=False,
        k=0.04
    )
    
    # Draw Good Features to Track on the original image
    gftt_corners_img = original_img_copy.copy()
    if gftt_corners is not None:
        for corner in gftt_corners:
            x, y = corner.ravel()
            cv2.circle(gftt_corners_img, (int(x), int(y)), 5, (0, 255, 0), -1)  # Green circles
    
    # Combined image with both corner types
    combined_corners_img = original_img_copy.copy()
    # Draw Harris corners in red
    for corner in corners:
        cv2.circle(combined_corners_img, corner, 5, (0, 0, 255), -1)
    # Draw Good Features to Track corners in green
    if gftt_corners is not None:
        for corner in gftt_corners:
            x, y = corner.ravel()
            cv2.circle(combined_corners_img, (int(x), int(y)), 5, (0, 255, 0), -1)
    
    def encode_image(img):
        if len(img.shape) == 2:  # If grayscale, convert to 3 channels for consistency
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        _, buffer = cv2.imencode('.jpg', img)
        return base64.b64encode(buffer).decode('utf-8')
    
    # Create grayscale versions for visualization
    gray_img_vis = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    smooth_img_vis = cv2.cvtColor(smooth_img, cv2.COLOR_GRAY2BGR)
    gradient_magnitude_vis = cv2.cvtColor(gradient_magnitude, cv2.COLOR_GRAY2BGR)
    harris_response_normalized_vis = cv2.cvtColor(harris_response_normalized, cv2.COLOR_GRAY2BGR)
    angle_response_normalized_vis = cv2.cvtColor(angle_response_normalized, cv2.COLOR_GRAY2BGR)
    
    response = {
        'original': encode_image(img),
        'grayscale': encode_image(gray_img_vis),
        'smooth': encode_image(smooth_img_vis),
        'gradient': encode_image(gradient_magnitude_vis),
        'harris': encode_image(harris_response_normalized_vis),
        'angle': encode_image(angle_response_normalized_vis),
        'harris_corners': encode_image(harris_corners_img),
        'gftt_corners': encode_image(gftt_corners_img),
        'combined_corners': encode_image(combined_corners_img)
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)