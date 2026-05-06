# 🛡️ Phishing URL Detection System

A machine learning-based Flask web application that detects whether a URL is legitimate or malicious (phishing) using extracted lexical features.

---

## 🚀 Features

- 🔍 **Detection:** Identify phishing URLs using a trained ML model.
- 🌐 **Web UI:** User-friendly interface for manual URL testing.
- ⚡ **Real-time API:** Predict URL safety via JSON-based POST requests.
- 🧠 **Feature Extraction:** Automatically extracts lexical attributes from URLs.

---

## 🏗️ Tech Stack

- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn, Pandas, NumPy
- **Frontend:** HTML5, CSS3

---

## 📂 Project Structure

```text
phishing-detector/
│
├── app.py              # Flask Application & API
├── train.py            # Script to train the ML model
├── features.py         # URL feature extraction logic
├── requirements.txt    # Python dependencies
├── model.pkl           # Saved ML model (Generated after training)
├── templates/          # HTML files for Web UI
└── data/               # Phishing and Benign datasets