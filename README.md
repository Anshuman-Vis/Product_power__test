# 🥗 ProductPower AI - Food Safety & Nutrition Analyzer

**ProductPower** is an advanced AI-powered food safety and nutrition label analyzer. It utilizes Optical Character Recognition (OCR), Large Language Models (LLM), and Machine Learning (ML) to extract product information, calculate health risk scores based on ingredients/additives, and verify regulatory compliance (FSSAI).

## 🚀 Key Features

* **🔍 AI-Powered OCR**: Automatically extracts text from food labels using EasyOCR.
* **🧠 Intelligent Parsing**: Uses `google/flan-t5` to structure unstructured label text into clean JSON data.
* **⚠️ Risk Assessment Engine**:
* Calculates a 0-100 health risk score.
* Maps ingredients against an **FSSAI-compliant additive database**.
* Uses a Machine Learning model (Random Forest) for predictive risk category classification.


* **⚖️ Regulatory Compliance**: Built-in regex-based FSSAI license validator.
* **🖥️ Dual Interface**:
* **Web App (Streamlit)**: Fast, data-heavy reporting with interactive charts.
* **Modern Web UI**: A custom-designed frontend with interactive 3D-style robotic arm animation and user-friendly scan visualization.


Deployed on -- https://anshumanprojectpower.streamlit.app/
you check here live working




---

## 📂 Project Structure

```text
productpower/
├── app.py                # Streamlit web interface
├── server.py             # Custom HTTP web server (API backend)
├── productpower.py       # Core logic class (LLM + OCR + ML orchestration)
├── additives_database.py # Database of food additives & risks
├── fssai_validator.py    # FSSAI license number extraction & validation
├── risk_scorer.py        # Health scoring algorithms
├── train_models.py       # ML Model training script
├── run.py                # Command-line runner utility
├── requirements.txt      # Project dependencies
├── static/               # Frontend assets
│   ├── index.html        # Main landing page
│   ├── app.js            # Frontend logic & robotic arm animation
│   └── styles.css        # Visual styles
└── models/               # Saved ML models (generated via train_models.py)

```

---

## 🛠️ Setup & Installation

1. **Clone the repository** (if not done already).
2. **Setup Virtual Environment**:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

```


3. **Install Dependencies**:
```bash
pip install -r requirements.txt

```


4. **Train the ML Models** (Required before first use):
```bash
python train_models.py

```



---

## 💻 How to Run

You have two ways to interact with the project:

### Option 1: Streamlit Dashboard (Recommended for Data Analysis)

This version is perfect for batch analysis, viewing comparison charts, and detailed safety reports.

```bash
streamlit run app.py

```

### Option 2: Custom Modern Web UI

This version uses the custom `server.py` and the interactive frontend found in `/static`.

```bash
python server.py
# Then open: http://localhost:8000

```

---

## 🧪 Tech Stack Details

* **Backend**: Python, `http.server`, Streamlit.
* **AI/ML**:
* **OCR**: `easyocr` (Text recognition).
* **LLM**: `transformers` (Flan-T5 for JSON extraction).
* **ML**: `scikit-learn` & `xgboost` (Random Forest Classifier for risk scores).


* **Frontend**: HTML5, Vanilla JavaScript (Canvas API for animations), CSS3.
* **Data Visualization**: `plotly`, `pandas`.

---

## ⚖️ License

This project is built for food safety research and educational purposes. Ensure all regulatory checks are verified against official government portals.

---

### Tips for development:

* **Updating the UI**: Modify `app.js` and `styles.css` in the static folder to change the robotic arm animations or layout.
* **Adding Additives**: Update `additives_database.py` if you need to add new INS codes or regulatory restrictions.
* **Retraining**: If you change the risk score formulas in `risk_scorer.py`, remember to run `train_models.py` again to update the `.pkl` models.
