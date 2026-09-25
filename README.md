# AI Road Damage & Lane Marking Assessment

An AI-powered pipeline for detecting road surface damage (potholes, cracks, etc.) and assessing lane marking quality from images, built on **YOLOv8**. Includes a Streamlit web demo, a mobile camera streaming mode, and automated PDF report generation.

## Features

- 🛣️ **Road damage detection** using fine-tuned YOLOv8 models (`yolov8n.pt`, `yolov8s.pt`)
- 🎯 **Lane marking quality assessment** (`lane_quality.py`), with geometric measurement via Inverse Perspective Mapping (`metric_ipm.py`)
- 📷 **Mobile streaming support** — run detection on a live phone camera feed (`mobile_stream.py`)
- 🗺️ **Road registry** for tracking/logging assessed road segments (`road_registry.py`)
- 📄 **Automated PDF report generation** (`report_generator.py`)
- 🖥️ **Interactive Streamlit web app** (`app/app.py`)
- 🧠 **Custom training pipeline** on your own dataset (`train.py`, `dataset.py`, `evaluate.py`)
- ✅ Setup verification script and unit tests included

## Project Structure

```
AI-Road-Damage-Lane-Marking-Assessment/
├── .gitignore
├── README.md
└── road-damage-detection-main/
    ├── app/
    │   ├── app.py                 # Streamlit web app (main demo UI)
    │   ├── mobile_stream.py       # Live detection from a mobile/IP camera stream
    │   └── tempCodeRunnerFile.py  # Editor temp file (safe to ignore/delete)
    │
    ├── data/
    │   ├── download_dataset.py    # Script to download the training dataset
    │   └── road_damage.yaml       # YOLO dataset config (classes, paths)
    │
    ├── models/
    │   └── rdd_exp/
    │       └── args.yaml          # Saved training run configuration/hyperparameters
    │
    ├── src/
    │   ├── __init__.py
    │   ├── dataset.py             # Dataset loading & preprocessing
    │   ├── evaluate.py            # Model evaluation / metrics
    │   ├── inference.py           # Core inference logic (used by main.py & app.py)
    │   ├── lane_quality.py        # Lane marking condition/quality scoring
    │   ├── metric_ipm.py          # Inverse Perspective Mapping for real-world measurements
    │   ├── model.py                # Model loading/wrapper utilities
    │   ├── report_generator.py    # Builds the PDF assessment report
    │   ├── road_registry.py       # Tracks/logs assessed road segments
    │   ├── train.py                # YOLOv8 training script
    │   └── utils.py                # Shared helper functions
    │
    ├── static/
    │   └── index.html              # Static web asset
    │
    ├── test_images/
    │   └── sample.jpg              # Sample image for quick testing
    │
    ├── tests/
    │   └── test_utils.py           # Unit tests
    │
    ├── check_setup.py              # Verifies environment/dependencies are correctly installed
    ├── config.yaml                  # Central pipeline configuration
    ├── main.py                      # Main CLI entry point for detection/assessment
    ├── requirements.txt
    ├── yolov8n.pt                   # YOLOv8 Nano weights (faster, lighter)
    └── yolov8s.pt                   # YOLOv8 Small weights (more accurate)
```

## Requirements

| Category | Libraries |
|---|---|
| Core ML / CV | `ultralytics==8.3.28`, `torch==2.4.1`, `torchvision==0.19.1`, `opencv-python==4.10.0.84`, `numpy==1.26.4`, `Pillow==10.4.0` |
| Data handling | `pandas==2.2.3`, `pyyaml==6.0.2`, `scikit-learn==1.5.2`, `albumentations==1.4.18` |
| Visualization / metrics | `matplotlib==3.9.2`, `seaborn==0.13.2` |
| Web app (demo) | `streamlit==1.39.0`, `streamlit-drawable-canvas==0.9.3` |
| Utilities | `tqdm==4.66.5`, `requests==2.32.3`, `fpdf2==2.7.9` |

- **Python:** 3.9–3.11 recommended (for `torch==2.4.1` / `ultralytics` compatibility)
- **GPU (optional):** CUDA-capable GPU recommended for faster inference/training; CPU works fine for inference

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/AayushSingh34/AI-Road-Damage-Lane-Marking-Assessment.git
cd AI-Road-Damage-Lane-Marking-Assessment/road-damage-detection-main

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify your setup
python check_setup.py
```

## Configuration

Pipeline behavior (model paths, thresholds, input/output directories, etc.) is controlled centrally via `config.yaml`:

```bash
nano config.yaml   # or open in your editor of choice
```

Dataset class names and paths for training/evaluation are defined separately in `data/road_damage.yaml`.

## Usage

### 1. Download the dataset (if training or re-evaluating)

```bash
python data/download_dataset.py
```

### 2. Run the main detection/assessment pipeline

```bash
python main.py
```

Uses `config.yaml` to determine input images, which model checkpoint to load (`yolov8n.pt` or `yolov8s.pt`), and where to write results. Under the hood this calls `src/inference.py` for detection, `src/lane_quality.py` + `src/metric_ipm.py` for lane assessment, and `src/report_generator.py` to produce the PDF report.

### 3. Run the Streamlit web demo

```bash
streamlit run app/app.py
```

Launches an interactive UI to upload or draw on road images and view damage + lane marking assessment results, with a downloadable PDF report.

### 4. Run live detection from a mobile/streaming camera

```bash
python app/mobile_stream.py
```

### 5. Train on your own data

```bash
python src/train.py
```

Training configuration and hyperparameters are saved to `models/rdd_exp/args.yaml` for reproducibility.

### 6. Evaluate a trained model

```bash
python src/evaluate.py
```

### 7. Run tests

```bash
pytest tests/
```

## Model Weights

Two YOLOv8 checkpoints are included at the project root:

- `yolov8n.pt` — Nano variant: faster inference, lower accuracy, good for mobile/live streaming
- `yolov8s.pt` — Small variant: better accuracy, slightly slower

Select which one to use via `config.yaml`.

## Output

Running the pipeline produces:
- Annotated images highlighting detected road damage and lane marking issues
- Lane marking quality metrics (via IPM-based real-world measurement)
- A PDF report (`report_generator.py`) summarizing the assessment for each processed input
- Optional logging of assessed segments via `road_registry.py`

## Sample Images

A sample test image is provided at `test_images/sample.jpg` to try the pipeline without your own data.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

<!-- fill in: e.g. MIT License -->

## Acknowledgements

- Built with [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
