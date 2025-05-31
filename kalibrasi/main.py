import cv2
import numpy as np
import time

CHECKERBOARD = (8, 5)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

objpoints = []
imgpoints = []

cap = cv2.VideoCapture(0)
img_count = 0
last_capture_time = 0  # waktu terakhir gambar ditambahkan

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    now = time.time()

    if found:  # jeda 1 detik
       
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        if   (now - last_capture_time > 1):
            objpoints.append(objp)
            imgpoints.append(corners2)
            
        cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, found)
        last_capture_time = now  # perbarui waktu terakhir
    frame = cv2.flip(frame, 1)

    cv2.imshow('Kalibrasi Kamera', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Kalibrasi kamera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("\nHasil Kalibrasi:")
print("Matriks Kamera (Intrinsik):\n", mtx)
print("Koefisien Distorsi:\n", dist)

# Simpan hasil kalibrasi
np.savez("kalibrasi_kamera.npz", mtx=mtx, dist=dist)