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
- **ML Model:** Random Forest

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
```
---

## ⚙️ Installation & Setup
## 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/phishing-detector.git
cd phishing-detector
```

## 2️⃣ Set up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Train the Model (If model.pkl is missing)

```bash
python train.py
```

## 5️⃣ Run the Application

```bash
python app.py
```

View the app at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## 🌐 API Usage
Endpoint: POST /predict
Payload:

```bash
{
  "url": "http://example-phish-site.com"
}
```

## 📊 Example Results

| URL | Result |
| :---         | :----         |
| https://en.wikipedia.org/wiki/Main_Page         | Safe           | 
| https://www.youtube.com/         | Safe           | 
| https://gemini.google.com/app         | Safe           | 
| www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd=_home-customer&nav=1/loading.php         | Phishing           | 
| https://steamcommunity-giveaway.my3gb.com/         | Phishing           | 
| http://tinyurl.com/bsebhuz         | Phishing           | 

## 📸 Screenshots

<img width="1920" height="1040" alt="Screenshot 2026-05-07 030448" src="https://github.com/user-attachments/assets/dff936fd-b8f0-42b9-9bfd-c0f957babf0e" />
<img width="1920" height="1040" alt="Screenshot 2026-05-07 030405" src="https://github.com/user-attachments/assets/5ebb0ade-1395-4e8c-ab71-2b4d9cafb1ce" />
<img width="1920" height="1040" alt="Screenshot 2026-05-07 030233" src="https://github.com/user-attachments/assets/2209f8e8-e233-4867-921c-90e350710b77" />



