# 🎭 Emotion Detection App  
> Real-time Facial Emotion Recognition + Background Music  
> Built with **DeepFace**, **TensorFlow**, **OpenCV**, and **Pygame**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![DeepFace](https://img.shields.io/badge/DeepFace-0.0.79-green.svg)](https://github.com/serengil/deepface)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🧠 Overview

**Emotion Detection App** adalah aplikasi pendeteksi emosi wajah real-time berbasis kamera menggunakan model **DeepFace**.  
Aplikasi ini menampilkan **emosi, usia, dan gender** secara langsung, serta memutar **musik sesuai mood** pengguna menggunakan **Pygame**.

> Dikembangkan untuk riset dan pembelajaran AI di **Politeknik AI Budi Mulia Dua**.

---

## ✨ Features

✅ Deteksi wajah dan ekspresi real-time  
✅ Prediksi emosi utama (`happy`, `sad`, `angry`, `fear`, `disgust`, `surprise`, `neutral`)  
✅ Tampilan visual interaktif dengan OpenCV  
✅ Statistik probabilitas emosi pada panel sisi kanan  
✅ Musik latar otomatis sesuai mood (looped per emosi)  
✅ Cross-platform: Ubuntu, macOS, Windows  

---



## 🧩 System Requirements

| Komponen | Rekomendasi | Catatan |
|-----------|--------------|---------|
| Python | **3.11.x** | Versi paling stabil untuk DeepFace 0.0.79 |
| OS | Ubuntu 22.04+, macOS 13+, Windows 10/11 | Semua didukung |
| CPU | Intel i5 / Ryzen 5 | GPU opsional |
| RAM | Minimal 8 GB | TensorFlow + OpenCV membutuhkan memori sedang |
| Kamera | Internal / USB Webcam | Default `device=0` |

---

## ⚙️ Installation Guide

### Windows

git clone https://github.com/rohbintang/deepfacesadata.git
cd emotion
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

### Ubuntu
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-opencv ffmpeg libasound-dev
git clone https://github.com/rohbintang/deepfacesadata.git
cd emotion
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

### MAC
brew install python@3.11
git clone https://github.com/rohbintang/deepfacesadata.git
cd emotion
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install tensorflow-macos==2.15.0 tensorflow-metal keras==2.15.0
pip install -r requirements.txt

### Running the App

Setelah environment aktif:

python emotion.py
