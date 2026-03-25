
# 🍃 EcoPack AI: Nexus Supply Chain Engine

<div align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite" />
  <img src="https://img.shields.io/badge/Framer_Motion-black?style=for-the-badge&logo=framer&logoColor=blue" alt="Framer Motion" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
</div>

<br/>

> **EcoPack AI** is an intelligent, full-stack supply chain simulation platform. It uses Machine Learning (Random Forest & XGBoost) to recommend the most sustainable and cost-effective packaging materials based on heavy industrial physical constraints, outputting data to a stunning, highly responsive 3D Eco-Futurist dashboard.

---

## ✨ Core Features

* **🧠 AI Recommendation Engine:** Predicts CO₂ footprints and dynamic manufacturing costs using trained ML models based on precise material physics (Tensile Strength, Biodegradability, Weight Capacity).
* **🌌 Eco-Futurist UI/UX:** A bespoke React dashboard featuring Framer Motion 3D tilt-cards, a custom bioluminescent mouse tracker, and cinematic boot sequences.
* **📊 Real-Time BI Analytics:** Interactive dual-axis charts comparing economic viability vs. environmental impact.
* **📱 True Responsive Design:** Flawlessly adapts from ultra-wide 4K monitors to mobile screens with intelligent CSS grid-stacking.
* **📄 One-Click PDF Reporting:** Generates pixel-perfect, dark-mode PDF snapshots of the dashboard using `html2pdf.js` for stakeholder meetings.

---

## 🏗️ System Architecture

1. **Client Layer:** React.js + Vite + Framer Motion + Recharts
2. **API Layer:** Flask REST API (`/api/recommend`)
3. **Intelligence Layer:** Scikit-Learn (Random Forest) & XGBoost (Cost/CO2 Prediction Models) + Custom Penalty Ranking Algorithm
4. **Data Layer:** PostgreSQL (Simulation logging and history)

---

## 🚀 Getting Started

Follow these steps to run the EcoPack AI Nexus Engine on your local machine.

### 1. Prerequisites
Make sure you have the following installed:
* [Node.js](https://nodejs.org/) (v20+)
* [Python](https://www.python.org/) (3.10+)
* PostgreSQL

### 2. Clone the Repository
```bash
git clone [https://github.com/ShameelMohamed/ECOPACK-AI.git](https://github.com/ShameelMohamed/ECOPACK-AI.git)
cd ECOPACK-AI

### 3. Backend Setup (Flask & AI Models)
*Note: Due to GitHub's file size limits, the trained >100MB `.pkl` models are not included in this repository. You must generate them locally first.*

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate # On Mac/Linux

# Install Python dependencies
pip install -r requirements.txt

# IMPORTANT: Train the ML models to generate the .pkl files
python train_models.py

# Start the Flask Server
python app.py
```
*The backend will boot up on `http://127.0.0.1:5000`*

### 4. Frontend Setup (React & Vite)
Open a **new** terminal window, keeping the Flask backend running.

```bash
# Navigate to the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```
*The UI will boot up on `http://localhost:5173`*

---

## 🧪 AI Simulation Test Cases
Want to see how the AI adapts to different industries? Try inputting these constraints into the dashboard:

| Industry Category | Capacity (kg) | Strength (MPa) | Bio-Score | Recycle % | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cosmetics** | 2 | 15 | 95 | 50 | *High Eco Focus (Agro-Waste, Plant-Based)* |
| **Electronics** | 25 | 120 | 50 | 85 | *Balanced Metrics (Recycled Kraft, Bio-Composite)* |
| **Heavy Automotive** | 1500 | 600 | 20 | 90 | *High Strength Priority (Recycled Metal/Composite)* |

---

## 👨‍💻 Developer & License

Developed by **Shameel Mohamed**
* 📧 Email: shameelmohamed2005@gmail.com
* 🐙 GitHub: [@ShameelMohamed](https://github.com/ShameelMohamed)

Licensed under the [MIT License](https://opensource.org/license/MIT). Feel free to use, modify, and distribute this project.

