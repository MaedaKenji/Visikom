import os

# Fungsi untuk menghapus file berlebih di dalam folder
def hapus_file_berlebih(folder_path, max_files=10):
    # Dapatkan daftar semua file di folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Jika jumlah file lebih dari batas maksimum
    if len(files) > max_files:
        # Urutkan file berdasarkan nama (opsional, bisa disesuaikan)
        files.sort()
        
        # Hitung berapa file yang harus dihapus
        files_to_remove = files[max_files:]
        
        # Hapus file yang berlebih
        for file_name in files_to_remove:
            file_path = os.path.join(folder_path, file_name)
            print(f"Menghapus file: {file_path}")
            os.remove(file_path)

# Direktori utama yang berisi folder Sample0 hingga Sample9
base_directory = "Datasets"

# Loop melalui folder Sample0 hingga Sample9
for i in range(10):
    folder_name = f"Sample{i}"
    folder_path = os.path.join(base_directory, folder_name)
    
    # Periksa apakah folder ada
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        print(f"Memproses folder: {folder_path}")
        hapus_file_berlebih(folder_path)
    else:
        print(f"Folder tidak ditemukan: {folder_path}")

print("Proses selesai.")