# Camera Calibration and Image Processing Toolkit

This repository contains a collection of tools and experiments for camera calibration, image processing, and computer vision, primarily using Python and React. It is organized into several directories, each focusing on a specific method or experiment.

## Repository Structure

- **Backup/**  
  Contains backup files and older versions of experiments, including manual CNN attempts.

- **HarrisMethode/**  
  Implements the Harris Corner Detection method and related image processing scripts.
  - `app.py`, `main.py`, `delete.py`: Python scripts for Harris method experiments.
  - `img.jpg`: Sample image for processing.
  - `my-app/`: A React + TypeScript + Vite frontend for visualization and interaction.

- **kalibrasi/**  
  Contains scripts and data for camera calibration.
  - `main.py`: Main calibration script.
  - `Computer-Engineering-1.jpg`: Sample calibration image.
  - `laporan.tex`: LaTeX report for documentation.
  - `output/`: Output files from calibration runs.

- **Manual CNN/**  
  Experiments with manually implemented Convolutional Neural Networks.
  - `main.ipynb`: Jupyter notebook for CNN experiments.
  - `model_color.npz`, `model_gray.npz`, `model_seratus.npz`: Saved model weights.
  - `prediction_comparison_*.csv`: Results and comparisons of predictions.

- **kalibrasi_kamera.npz**  
  Numpy archive containing camera calibration parameters.

- **Readme.md**  
  This file.

## Features

- Camera calibration using Python and OpenCV.
- Harris Corner Detection implementation and visualization.
- Manual CNN experiments for image classification.
- React + TypeScript + Vite frontend for interactive demos.

## Getting Started

1. **Python Scripts**  
   Navigate to the relevant directory and run the Python scripts (e.g., `python main.py`).

2. **Frontend (React + Vite)**
   ```
   cd HarrisMethode/my-app
   npm install
   npm run dev
   ```
   Then open the provided local URL in your browser.

## Requirements

- Python 3.x
- NumPy, OpenCV, and other dependencies (see individual script requirements)
- Node.js and npm (for the frontend)

## License

This project is for educational and research purposes.

---

Feel free to explore each directory for more details and experiment with the provided scripts and notebooks.