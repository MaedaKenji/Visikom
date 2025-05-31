import os
import shutil
import cv2

def copy_and_resize_images(source_root, target_root, image_size=(100, 100)):
    os.makedirs(target_root, exist_ok=True)
    
    for i in range(10):  # Iterasi Sample0 hingga Sample9
        source_dir = os.path.join(source_root, f"Sample{i}")
        target_dir = os.path.join(target_root, f"Sample{i}")
        os.makedirs(target_dir, exist_ok=True)
        
        files = sorted(os.listdir(source_dir))[:100]  # Ambil 100 file pertama
        
        for file_name in files:
            src_file = os.path.join(source_dir, file_name)
            dst_file = os.path.join(target_dir, file_name)
            
            if os.path.isfile(src_file):
                # Baca dan resize gambar
                image = cv2.imread(src_file, cv2.IMREAD_UNCHANGED)
                resized_image = cv2.resize(image, image_size, interpolation=cv2.INTER_AREA)
                
                # Simpan ke direktori tujuan
                cv2.imwrite(dst_file, resized_image)
                print(f"Processed: {dst_file}")
            else:
                print(f"File not found: {src_file}")

if __name__ == "__main__":
    source_path = "Datasets/numbers/mnist_png/Hnd/"
    target_path = "Datasets/SizeSeratus/numbers/mnist_png"
    copy_and_resize_images(source_path, target_path)
