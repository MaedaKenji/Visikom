import cv2
import numpy as np
import os
import csv
import datetime

def load_data(dataset_path='Datasets/SizeSeratus/numbers/mnist_png'):
    X = []
    y = []
    for digit in range(10):
        folder = os.path.join(dataset_path, f"Sample{digit}")
        if not os.path.isdir(folder):
            print(f"Folder {folder} tidak ditemukan.")
            continue
        for filename in os.listdir(folder):
            if filename.endswith('.png'):
                filepath = os.path.join(folder, filename)
                img = cv2.imread(filepath)
                if img is None:
                    continue
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
    one_hot[np.arange(y.shape[0]), y] = 1
    return one_hot
def softmax(z):
    """
    Fungsi softmax untuk mengubah output linear menjadi probabilitas.
    Dikurangi nilai maksimum tiap baris untuk kestabilan numerik.
    """
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)
def save_model(model, filename="model_color.npz"):
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
    print(f"y: {y}")
    n_classes = 10
    W = np.random.randn(n_features, n_classes) * 0.01
    b = np.zeros((1, n_classes))
    y_encoded = one_hot_encode(y, n_classes)
    print(f"y_encoded: {y_encoded}")
    log_data = []
    for epoch in range(epochs):
        Z = np.dot(X, W) + b
        A = softmax(Z)
        loss = -np.sum(y_encoded * np.log(A + 1e-8)) / n_samples
        dZ = A - y_encoded
        dW = np.dot(X.T, dZ) / n_samples
        db = np.sum(dZ, axis=0, keepdims=True) / n_samples
        W -= learning_rate * dW
        b -= learning_rate * db
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
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"training_log_detailed_{timestamp}.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ["Epoch", "X", "Y_Label", "W", "b", "net", "fnet", "dw", "dz", "db"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in log_data:
            writer.writerow(row)
    print(f"Detailed log training disimpan ke file {csv_filename}")
    def net(x):
        return np.dot(x, W) + b
    def netfunction(x):
        z = net(x)
        return softmax(z)
    model = {
        'W': W,
        'b': b,
        'net': net,
        'netfunction': netfunction
    }
    return model
X, y = load_data()
print("Data berhasil dimuat. Shape X:", X.shape, ", Shape y:", y.shape)
model = train_nn(X, y, learning_rate=0.1, epochs=100)
import numpy as np
import pandas as pd
import datetime
predicted_classes = []
actual_classes = []
for i in range(1000):
    sample = X[i].reshape(1, -1)
    net_value = model['net'](sample)
    fnet_value = model['netfunction'](sample)
    predicted_class = np.argmax(fnet_value)
    predicted_classes.append(predicted_class)
    actual_classes.append(y[i])
df = pd.DataFrame({
    'Predicted Class': predicted_classes,
    'Actual Class': actual_classes
})
df['Error'] = df['Predicted Class'] != df['Actual Class']
accuracy = (df['Predicted Class'] == df['Actual Class']).mean() * 100
print(f"Akurasi prediksi: {accuracy:.2f}%")
print(df)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"prediction_comparison_{timestamp}.csv"
df.to_csv(csv_filename, index=False)
print(f"CSV file telah disimpan dengan nama: {csv_filename}")
print("Input shape: ", X.shape)
print("Image shape: ", X[0].shape)
save_model(model, "model_seratus.npz")
print("Bias shape: ", model['b'].shape)
print("Weight shape: ", model['W'].shape)
with open("prediction_details.txt", "w") as f:
    f.write("Net (nilai linear):\n")
    f.write(np.array2string(net_value, precision=4, separator=', ') + "\n\n")
    f.write("fnet (hasil softmax):\n")
    f.write(np.array2string(fnet_value, precision=4, separator=', ') + "\n")
    f.write("\nWeight:\n")
    f.write(np.array2string(model['W'], precision=4, separator=', ') + "\n\n")
    f.write("Bias:\n")
    f.write(np.array2string(model['b'], precision=4, separator=', ') + "\n")
print("Detail prediksi disimpan ke file prediction_details.txt")
