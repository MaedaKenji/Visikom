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

# Fungsi untuk mengubah nama subfolder
def ubah_nama_subfolder(base_directory, prefix_lama="Sample", prefix_baru="Dataset"):
    # Loop melalui folder Sample0 hingga Sample9
    for i in range(10):
        folder_lama = f"{prefix_lama}{i}"
        folder_baru = f"{prefix_baru}{i}"
        
        # Path lengkap untuk folder lama dan baru
        folder_path_lama = os.path.join(base_directory, folder_lama)
        folder_path_baru = os.path.join(base_directory, folder_baru)
        
        # Periksa apakah folder lama ada
        if os.path.exists(folder_path_lama) and os.path.isdir(folder_path_lama):
            print(f"Mengubah nama folder: {folder_path_lama} -> {folder_path_baru}")
            os.rename(folder_path_lama, folder_path_baru)
        else:
            print(f"Folder tidak ditemukan: {folder_path_lama}")

# Direktori utama yang berisi folder Sample0 hingga Sample9
base_directory = "Datasets"

# Menampilkan menu pilihan fitur kepada pengguna
print("Pilih fitur yang ingin digunakan:")
print("1. Menghapus file berlebih di dalam folder")
print("2. Mengubah nama subfolder")
print("3. Jalankan kedua fitur di atas")
pilihan = input("Masukkan nomor pilihan (1/2/3): ")

# Proses berdasarkan pilihan pengguna
if pilihan == "1":
    print("Memulai proses menghapus file berlebih...")
    for i in range(10):
        folder_name = f"Sample{i}"  # Nama folder asli
        folder_path = os.path.join(base_directory, folder_name)
        
        # Periksa apakah folder ada
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            print(f"Memproses folder: {folder_path}")
            hapus_file_berlebih(folder_path)
        else:
            print(f"Folder tidak ditemukan: {folder_path}")
elif pilihan == "2":
    print("Memulai proses mengubah nama subfolder...")
    ubah_nama_subfolder(base_directory, prefix_baru="Sepuluh")
elif pilihan == "3":
    print("Memulai proses mengubah nama subfolder...")
    ubah_nama_subfolder(base_directory)
    
    print("\nMemulai proses menghapus file berlebih...")
    for i in range(10):
        folder_name = f"Dataset{i}"  # Nama folder setelah diubah
        folder_path = os.path.join(base_directory, folder_name)
        
        # Periksa apakah folder ada
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            print(f"Memproses folder: {folder_path}")
            hapus_file_berlebih(folder_path)
        else:
            print(f"Folder tidak ditemukan: {folder_path}")
else:
    print("Pilihan tidak valid. Program berhenti.")

print("Proses selesai.")