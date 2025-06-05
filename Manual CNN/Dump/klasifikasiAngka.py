import cv2
import numpy as np
import os
import csv
import datetime

def load_data(dataset_path='Datasets'):
    """
    Fungsi untuk memuat data dari folder dataset.
    Setiap folder (Sample0, Sample1, …, Sample9) mewakili kelas angka.
    Citra dibaca dalam mode grayscale, diflatten dan dinormalisasi.
    """
    X = []
    y = []
    # Lakukan iterasi untuk setiap kelas digit 0-9
    for digit in range(10):
        folder = os.path.join(dataset_path, f"Sample{digit}")
        # Pastikan folder ada
        if not os.path.isdir(folder):
            print(f"Folder {folder} tidak ditemukan.")
            continue
        for filename in os.listdir(folder):
            if filename.endswith('.png'):
                filepath = os.path.join(folder, filename)
                # Baca gambar dalam grayscale
                img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                # Flatten citra menjadi vektor 1D dan normalisasi nilai piksel ke [0,1]
                img_flat = img.flatten().astype(np.float32) / 255.0
                X.append(img_flat)
                y.append(digit)
    X = np.array(X)
    y = np.array(y)
    print(f"img shape {img.shape}")
    print(f"img flat : {X[0].shape}")
    return X, y

def one_hot_encode(y, num_classes=10):
    """
    Mengubah label y menjadi format one-hot.
    """
    one_hot = np.zeros((y.shape[0], num_classes))
    # print("One hot before: ", one_hot)
    one_hot[np.arange(y.shape[0]), y] = 1
    # print("One hot after: ", one_hot)
    return one_hot

def softmax(z):
    """
    Fungsi softmax untuk mengubah output linear menjadi probabilitas.
    Dikurangi nilai maksimum tiap baris untuk kestabilan numerik.
    """
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    # print(f"exp_z: {exp_z} np.max: {np.max(z, axis=1, keepdims=True)} np.sum: {np.sum(exp_z, axis=1, keepdims=True)}") 
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

def save_model(model, filename="model.npz"):
    """
    Menyimpan model ke file NPZ.
    Parameter yang disimpan adalah weight (W) dan bias (b).
    """
    np.savez(filename, W=model['W'], b=model['b'])
    print(f"Model disimpan ke file {filename}")
    
def load_model(filename="model.npz"):
    """
    Memuat model dari file NPZ.
    Mengembalikan dictionary dengan weight (W), bias (b),
    dan fungsi net serta netfunction untuk prediksi.
    """
    data = np.load(filename)
    W = data['W']
    b = data['b']
    
    def net(x):
        return np.dot(x, W) + b

    def netfunction(x):
        # Pastikan fungsi softmax sudah didefinisikan
        return softmax(net(x))
    
    model = {
        'W': W,
        'b': b,
        'net': net,
        'netfunction': netfunction
    }
    print(f"Model berhasil dimuat dari file {filename}")
    return model

def train_nn(X, y, learning_rate=0.01, epochs=100):
    """
    Fungsi training untuk model klasifikasi:
      - Inisialisasi bobot dan bias
      - Lakukan forward pass (net = X.W + b) dan hitung softmax (fnet)
      - Hitung loss cross-entropy
      - Hitung gradien (dz, dw, db) dengan backpropagation
      - Update parameter menggunakan gradient descent
      
    Log training per epoch disimpan ke file CSV dengan kolom:
      Epoch, X, Y_Label, W, b, net, fnet, dw, dz, db
      
    Note: Untuk menghindari log data yang terlalu besar, hanya nilai sample pertama (index 0)
    yang dijadikan representasi.
    """
    n_samples, n_features = X.shape
    print(f"n_samples: {n_samples}, n_features: {n_features}")
    n_classes = 10

    # Inisialisasi bobot dan bias
    W = np.random.randn(n_features, n_classes) * 0.01
    b = np.zeros((1, n_classes))

    # Ubah label ke format one-hot
    y_encoded = one_hot_encode(y, n_classes)
    # print(f"y_encoded: {y_encoded}")
    # print(f"y_encoded shape: {y_encoded.shape}")

    # List untuk menyimpan log per epoch
    log_data = []

    for epoch in range(epochs):
        # Forward pass
        Z = np.dot(X, W) + b       # net input
        A = softmax(Z)             # fnet, output probabilitas

        # Hitung loss cross-entropy
        loss = -np.sum(y_encoded * np.log(A + 1e-8)) / n_samples

        # Backpropagation
        dZ = A - y_encoded         # error (dz)
        dW = np.dot(X.T, dZ) / n_samples   # gradien bobot
        db = np.sum(dZ, axis=0, keepdims=True) / n_samples  # gradien bias

        # Update parameter
        W -= learning_rate * dW
        b -= learning_rate * db

        # Simpan log untuk epoch ini, ambil nilai sample pertama sebagai contoh
        log_data.append({
            "Epoch": epoch,
            "X": np.array2string(X[0], precision=2, separator=','),
            "Y_Label": y[0],
            "W": np.array2string(W, precision=4, separator=','),
            "b": np.array2string(b, precision=4, separator=','),
            "net": np.array2string(Z[0], precision=4, separator=','),
            "fnet": np.array2string(A[0], precision=4, separator=','),
            "dw": np.array2string(dW, precision=4, separator=','),
            "dz": np.array2string(dZ[0], precision=4, separator=','),
            "db": np.array2string(db, precision=4, separator=',')
        })

        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{epochs}, Loss: {loss:.4f}")

    # Simpan log training ke file CSV
    # Tambahkan timestamp ke nama file log
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"training_log_detailed_{timestamp}.csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ["Epoch", "X", "Y_Label", "W", "b", "net", "fnet", "dw", "dz", "db"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in log_data:
            writer.writerow(row)
    print(f"Detailed log training disimpan ke file {csv_filename}")

    # Definisikan fungsi net dan netfunction untuk keperluan prediksi
    def net(x):
        return np.dot(x, W) + b

    def netfunction(x):
        z = net(x)
        return softmax(z)

    # Kembalikan model
    model = {
        'W': W,
        'b': b,
        'net': net,
        'netfunction': netfunction
    }
    return model

def main():
    # Memuat data dari folder dataset
    X, y = load_data()
    print("Data berhasil dimuat. Shape X:", X.shape, ", Shape y:", y.shape)

    # Training model dengan parameter tertentu (misal: learning_rate=0.1, epochs=100)
    model = train_nn(X, y, learning_rate=0.1, epochs=100)

    # Contoh prediksi untuk data pertama
    sample = X[0].reshape(1, -1)
    net_value = model['net'](sample)           # Nilai linear (net)
    fnet_value = model['netfunction'](sample)    # Output softmax (fnet)
    predicted_class = np.argmax(fnet_value)
    save_model(model, "model.npz")
    print("Prediksi kelas untuk sample pertama:", predicted_class)
    print("Bias shape: ", model['b'].shape)
    print("Weight shape: ", model['W'].shape)

    # Simpan nilai prediksi (net dan fnet) ke file teks
    with open("prediction_details.txt", "w") as f:
        f.write("Prediksi untuk sample pertama:\n")
        f.write(f"Predicted Class: {predicted_class}\n\n")
        f.write("Net (nilai linear):\n")
        f.write(np.array2string(net_value, precision=4, separator=', ') + "\n\n")
        f.write("fnet (hasil softmax):\n")
        f.write(np.array2string(fnet_value, precision=4, separator=', ') + "\n")
        # Write nilai weight dan bias
        f.write("\nWeight:\n")
        f.write(np.array2string(model['W'], precision=4, separator=', ') + "\n\n")
        f.write("Bias:\n")
        f.write(np.array2string(model['b'], precision=4, separator=', ') + "\n")
    print("Detail prediksi disimpan ke file prediction_details.txt")

if __name__ == "__main__":
    main()
