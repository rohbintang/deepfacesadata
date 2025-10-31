# 🎭 Emotion Detection App  
> Real-time Facial Emotion Recognition + Background Music  
> Built with **DeepFace**, **TensorFlow**, **OpenCV**, and **Pygame**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![DeepFace](https://img.shields.io/badge/DeepFace-0.0.79-green.svg)](https://github.com/serengil/deepface)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🧠 Overview
**Emotion Detection App** adalah aplikasi pendeteksi emosi wajah real-time berbasis kamera menggunakan **DeepFace**.  
Menampilkan **emosi, usia, gender**, dan memutar **musik sesuai mood** dengan **Pygame**.  
Dikembangkan untuk riset dan pembelajaran AI di **Politeknik AI Budi Mulia Dua**.

---

## ✨ Features
- Deteksi wajah & ekspresi real-time  
- Prediksi emosi utama: happy, sad, angry, fear, disgust, surprise, neutral  
- Tampilan interaktif dengan OpenCV  
- Statistik probabilitas emosi  
- Musik latar sesuai mood  
- Cross-platform (Ubuntu, macOS, Windows)

---

## 🧩 System Requirements
| Komponen | Rekomendasi | Catatan |
|-----------|--------------|---------|
| Python | **3.11.x** | Paling stabil untuk DeepFace 0.0.79 |
| OS | Ubuntu 22.04+, macOS 13+, Windows 10/11 | Semua didukung |
| CPU | Intel i5 / Ryzen 5 | GPU opsional |
| RAM | ≥ 8 GB | TensorFlow + OpenCV butuh memori sedang |
| Kamera | Internal / USB Webcam | Default `device=0` |

---

## ⚙️ Installation Guide

### 🪟 Windows
```bash
git clone https://github.com/rohbintang/deepfacesadata.git
cd emotion
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 🐧 Ubuntu / Linux
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-opencv ffmpeg libasound-dev
git clone https://github.com/rohbintang/deepfacesadata.git
cd emotion
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 🍎 macOS
```bash
brew install python@3.11
git clone https://github.com/rohbintang/deepfacesadata.git
cd emotion
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install tensorflow-macos==2.15.0 tensorflow-metal keras==2.15.0
pip install -r requirements.txt
```

### 🚀 Running the App
Setelah environment aktif:
```bash
python emotion.py
```
Tekan **`q`** untuk keluar, **`c`** untuk menyimpan snapshot kamera.

---

## 📦 Dependencies (requirements.txt)
```txt
tensorflow==2.15.0.post1
keras==2.15.0
protobuf<4
h5py<3.11
numpy==1.26.4
deepface==0.0.79
retina-face==0.0.17
mtcnn==1.0.0
opencv-python==4.10.0.84
pygame==2.6.1
pillow<10
pandas==2.2.2
tqdm==4.66.5
python-dateutil==2.9.0.post0
typing_extensions==4.12.2
requests==2.32.3
Flask==3.1.2
Werkzeug==3.1.3
itsdangerous==2.2.0
Jinja2==3.1.6
gunicorn==23.0.0
packaging==24.0
wrapt<1.15
six==1.16.0
```

---

## 🎵 Emotion Audio Setup
Masukkan file MP3 di folder yang sama dengan `emotion.py`:
```
happy.mp3
sad.mp3
angry.mp3
fear.mp3
disgust.mp3
surprise.mp3
neutral.mp3
```
Kalau file tidak ada, app tetap jalan tanpa musik.  
Gunakan musik bebas lisensi dari:
- https://pixabay.com/music  
- https://mixkit.co/free-stock-music/

---


```

---

## 🧠 Troubleshooting
| Masalah | Penyebab | Solusi |
|----------|-----------|--------|
| `ModuleNotFoundError: cv2` | OpenCV belum terinstal | `pip install opencv-python` |
| `ImportError: LocallyConnected2D` | Keras 3 tidak kompatibel | Gunakan `keras==2.15.0` |
| `pygame.mixer` error | Tidak ada audio device | Jalankan di mesin dengan speaker |
| Kamera tidak terbuka | Device salah | `cv2.VideoCapture(1)` |
| “GPU will not be used” | Tidak ada CUDA | Aman diabaikan (CPU mode) |

---

## 🧩 Export Environment Snapshot
```bash
pip freeze > requirements-final.txt
```
Install ulang di mesin lain:
```bash
pip install -r requirements-final.txt
```

---

## 🧰 Tips
- Gunakan Python 3.11  
- Aktifkan virtual env (`venv`)  
- Tutup aplikasi lain yang pakai kamera (Zoom, OBS)  
- Simpan audio di folder `emotion`

---

## 🧑‍💻 Developer Notes
Struktur:
```
emotion/
 ├── emotion.py
 ├── requirements.txt
 ├── README.md
 ├── happy.mp3
 ├── sad.mp3
 └── ...
```


