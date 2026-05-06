from flask import Flask, request, jsonify, render_template
import joblib
from features import extract_features
import shap
import numpy as np
import traceback

app = Flask(__name__)

# Load the model
try:
    model = joblib.load("model.pkl")
    # Initialize the SHAP explainer once at startup to save time
    explainer = shap.TreeExplainer(model)
except Exception as e:
    print(f"Error loading model or explainer: {e}")

# MUST match the order in features.py EXACTLY
feature_names = [
    "url_length", "domain_length", "num_hyphens", "num_at",
    "num_qmark", "num_and", "num_equals", "digits", "letters", "specials",
    "digit_ratio", "letter_ratio", "subdomains",
    "too_many_subdomains", "suspicious_subdomain", "is_https",
    "has_suspicious_word", "has_suspicious_tld", "long_domain",
    "many_hyphens", "is_ip", "entropy", "is_top_domain"
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({"error": "No URL provided"}), 400

        url = data['url'].strip()
        
        # 1. Extract Features
        features = extract_features(url)
        X_input = np.array([features]) 

        # 2. Model Prediction
        pred = int(model.predict(X_input)[0])
        proba = model.predict_proba(X_input)[0]
        confidence = float(max(proba))

        # 3. SHAP Explanation
        shap_values = explainer.shap_values(X_input)

        # SHAP version handling: 
        if isinstance(shap_values, list):
            shap_vals = shap_values[1][0]
        else:
            if len(shap_values.shape) == 3:
                shap_vals = shap_values[0, :, 1]
            else:
                shap_vals = shap_values[0]

        # 4. Build Contributions
        contributions = []
        for name, val in zip(feature_names, shap_vals):
            contributions.append({
                "feature": name,
                "impact": round(float(val), 4)
            })

        top_contributions = sorted(
            contributions,
            key=lambda x: abs(x["impact"]),
            reverse=True
        )[:23]

        return jsonify({
            "prediction": "phishing" if pred == 1 else "safe",
            "confidence": round(confidence, 2),
            "explanations": top_contributions,
            "status": "success"
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)