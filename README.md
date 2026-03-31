
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


> **EcoPack AI** is an intelligent, full-stack supply chain simulation platform. It uses an advanced **3-Model Machine Learning Pipeline** (XGBoost & Random Forest) to evaluate physical constraints, apply industry-specific supply chain multipliers, and recommend the most sustainable and cost-effective packaging materials. Results are outputted to a stunning, highly responsive 3D Eco-Futurist dashboard.

-----

## ✨ Core Features

  * **🧠 3-Tier AI Recommendation Engine:** \* **The Physics Gatekeeper:** Filters out structurally non-viable materials based on Tensile Strength and Weight Capacity.
      * **Dynamic Estimators:** Accurately predicts CO₂ footprints and manufacturing costs using strictly bounded Industry Multipliers (e.g., Healthcare premiums vs. Agriculture discounts).
      * **Penalty Ranking System:** A custom mathematical algorithm that balances cost efficiency against the user's explicit environmental targets (Biodegradability and Recyclability).
  * **🌌 Eco-Futurist UI/UX:** A bespoke React dashboard featuring Framer Motion 3D tilt-cards, a custom bioluminescent mouse tracker, and cinematic boot sequences.
  * **📊 Real-Time BI Analytics:** Interactive dual-axis charts comparing economic viability vs. environmental impact.
  * **📱 True Responsive Design:** Flawlessly adapts from ultra-wide 4K monitors to mobile screens with intelligent CSS grid-stacking.
  * **📄 One-Click PDF Reporting:** Generates pixel-perfect, dark-mode PDF snapshots of the dashboard for stakeholder meetings.

-----

## 🏗️ System Architecture

1.  **Client Layer:** React.js + Vite + Framer Motion + Recharts
2.  **API Layer:** Flask REST API (`/api/recommend`)
3.  **Intelligence Layer:** \* **Model 1:** XGBoost Material Classifier (Physics Gatekeeper)
      * **Model 2:** Random Forest Regressor (Cost Predictor)
      * **Model 3:** XGBoost Regressor (CO₂ Estimator)
4.  **Data Layer:** PostgreSQL (Simulation logging and timestamped history)

-----

## 📈 AI Model Performance

The engine is powered by a custom-generated 10,000-row structured dataset, trained to natively understand physical limitations and real-world supply chain economics.

  * **🛡️ Material Classifier (XGBoost Physics Gatekeeper)**
      * **Accuracy:** `78.05%` *(Successfully eliminates weak materials from heavy industrial scenarios)*
  * **💰 Cost Predictor (Random Forest Regressor)**
      * **R² Score:** `0.9865` *(Optimal target: 0.90 to 0.98)*
      * **RMSE:** `838.96`
  * **🌱 CO₂ Estimator (XGBoost Regressor)**
      * **R² Score:** `0.9935` *(Optimal target: 0.90 to 0.98)*
      * **RMSE:** `42.36`

-----

## 🚀 Getting Started

Follow these steps to run the EcoPack AI Nexus Engine on your local machine.

### 1\. Prerequisites

Make sure you have the following installed:

  * [Node.js](https://nodejs.org/) (v20+)
  * [Python](https://www.python.org/) (3.10+)
  * PostgreSQL

### 2\. Clone the Repository

```bash
git clone https://github.com/ShameelMohamed/ECOPACK-AI.git
cd ECOPACK-AI
```

### 3\. Backend Setup (Flask & AI Models)

*Note: Due to GitHub's file size limits, the trained `.pkl` models and generated dataset are not included in the repository. You must train them locally first.*

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate # On Mac/Linux

# Install Python dependencies
pip install -r requirements.txt

# IMPORTANT: Generate the dataset and train the 3-model ML pipeline
python train_models.py

# Start the Flask Server
python app.py
```

*The backend will boot up on `http://127.0.0.1:5000`*

### 4\. Frontend Setup (React & Vite)

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

-----

## 🧪 AI Simulation Test Cases

Want to see how the AI adapts to extreme physics and industry conditions? Try inputting these constraints into the dashboard:

| Scenario | Industry | Load (kg) | Strength (MPa) | Eco-Targets (Bio / Recy) | Expected AI Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sterile Medical Tray** | Healthcare | 0.5 | 30 | 80 / 40 | *Applies Healthcare pricing premium. Recommends lightweight Biopolymers & Plant-Based materials.* |
| **E-Commerce Box** | E-commerce | 5 | 40 | 60 / 85 | *Applies volume discounts. Battles between Recycled Fiber and Recycled Plastics.* |
| **Heavy Engine Part** | Automotive | 150 | 500 | 2 / 95 | *Gatekeeper activates. Eliminates weak bio-materials, forcing Recycled Metals and heavy Composites.* |
| **Steel Construction Beam** | Construction | 600 | 700 | 5 / 90 | *Ultimate Gatekeeper stress test. Outputs only industrial-grade materials to safely handle massive loads.* |



## 👨‍💻 Developer & License

Developed by **Shameel Mohamed**

  * 📧 Email: shameelmohamed2005@gmail.com
  * 🐙 GitHub: [@ShameelMohamed](https://github.com/ShameelMohamed)

Licensed under the [MIT License](https://opensource.org/license/MIT). Feel free to use, modify, and distribute this project.