import cv2
import numpy as np

# Baca gambar
img = cv2.imread('coba.png')

# Periksa apakah gambar berhasil dibaca
if img is None:
    print("Gagal membaca gambar. Pastikan path file benar.")
else:
    # # Tampilkan gambar
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Cetak dimensi gambar
    print(f"Dimensi gambar: {img.shape}")  # (tinggi, lebar, channel)

    # Cetak semua nilai matriks
    # print("Nilai matriks gambar:")
    # for i in range(img.shape[0]):  # Iterasi tinggi (baris)
    #     for j in range(img.shape[1]):  # Iterasi lebar (kolom)
    #         pixel = img[i, j]  # Ambil nilai pixel di posisi (i, j)
    #         print(f"Pixel di posisi ({i}, {j}): {pixel}")
    print (f"Img asli : {img}")
    # print(img[0])
    # print(img[0][0])
    # print(img[0][0][0])
    print (img.shape)
    
    img_flat = img.flatten().astype(np.float32) / 255.0
    print(f"img flat : {img_flat}")
    print(img_flat.shape)