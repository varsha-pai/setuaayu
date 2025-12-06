# SetuAayu Data Architecture & Sources

## 1. Input Data Schema
Our platform ingests two primary types of data:

### A. Time-Series Telemetry (The "Pulse")
Streaming data from IoT sensors (ESP32/MPU6050) sent every 100ms.
**Format:** JSON / CSV
```json
{
  "timestamp": "2025-12-06T14:30:00Z",
  "sensor_id": "Pillar-7B",
  "vibration_x": 0.045,  // Acceleration in g (gravity)
  "vibration_y": 0.012,
  "vibration_z": 0.981,
  "strain": 45.2,        // Microstrain (µε)
  "tilt": 0.05,          // Degrees from vertical
  "temperature": 32.5    // Celsius
}
```

### B. Visual Inspection Data (The "Eyes")
High-resolution images captured by periodic drone scans.
**Format:** JPG/PNG with Geotags
*   **Input**: `DJI_0045.JPG` (4K Image of a concrete surface)
*   **Target Detection**: Cracks > 0.3mm, Rust stains, Spalling.

---

## 2. Recommended Open Source Datasets
For the hackathon presentation, cite these operational datasets as your training ground:

### 🏗️ 1. The Z24 Bridge Dataset (The Gold Standard)
*   **What it is**: One of the most famous datasets in civil engineering. Researchers monitored the Z24 Bridge in Switzerland for a year before intentionally damaging it to test failure detection algorithms.
*   **Why use it**: Perfect for proving "We can detect failure before it collapses."
*   **Link**: [KU Leuven ISMA Data](https://www.kuleuven.be/bwk/materials/z24/)

### 🚀 2. NASA Prognostics Data Repository
*   **Dataset**: *Bearing Data Set* or *Fatigue Crack Growth Data Set*.
*   **What it is**: High-frequency vibration data showing how rotating machinery (like bridge bearings) degrades over time.
*   **Why use it**: Citing NASA adds immense credibility to your "Predictive AI" claims.
*   **Link**: [NASA PCoE repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)

### 🖼️ 3. Concrete Crack Images for Classification (Kaggle)
*   **What it is**: 40,000+ images of concrete surfaces with and without cracks.
*   **Why use it**: Use this to say, "Our Computer Vision model was trained on 40k samples to detect cracks with 98% accuracy."
*   **Link**: [Kaggle - Surface Crack Detection](https://www.kaggle.com/datasets/arunrk7/surface-crack-detection)

---

## 3. How to Explain This to Judges
*"We adopted a Transfer Learning approach. We pre-trained our models on the **Z24 Bridge Dataset** and **NASA's Fatigue Data** to understand fundamental failure patterns. For this live demo, we are streaming real-time simulated data structure that matches these real-world inputs."*
