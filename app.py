from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# ===============================
# SAFE FUNCTIONS
# ===============================
def safe_int(x):
    try:
        return int(x)
    except:
        return 0

def safe_float(x):
    try:
        return float(x)
    except:
        return 0.0

# ===============================
# CONDITION ENGINE (MAIN LOGIC)
# ===============================
def evaluate_conditions(data, temp, appetite):

    vomiting = safe_int(data.get("vomiting"))
    diarrhea = safe_int(data.get("diarrhea"))
    coughing = safe_int(data.get("coughing"))
    skin = safe_int(data.get("skin"))
    weight = safe_int(data.get("weight"))

    results = []

    # Gastro
    if vomiting and diarrhea:
        score = 80 + temp
        results.append({
            "disease": "Gastroenteritis",
            "treatment": "Fluids + antiemetics",
            "score": score
        })

    if vomiting and diarrhea and temp > 38:
        score = 90 + temp
        results.append({
            "disease": "Severe Gastroenteritis",
            "treatment": "IV fluids + monitoring",
            "score": score
        })

    # Respiratory
    if coughing and temp > 38:
        score = 85 + temp
        results.append({
            "disease": "Respiratory Infection",
            "treatment": "Antibiotics + steam therapy",
            "score": score
        })

    if coughing and weight:
        score = 82
        results.append({
            "disease": "Chronic Respiratory Disease",
            "treatment": "Long-term care + nutrition",
            "score": score
        })

    # Skin
    if skin:
        results.append({
            "disease": "Skin Infection",
            "treatment": "Topical ointment",
            "score": 75
        })

    if skin and weight:
        results.append({
            "disease": "Severe Skin Infection",
            "treatment": "Antifungal + medicated bath",
            "score": 85
        })

    # Nutrition
    if weight and appetite == "Low":
        results.append({
            "disease": "Malnutrition",
            "treatment": "High-protein diet",
            "score": 78
        })

    # High fever cases
    if vomiting and temp > 39:
        results.append({
            "disease": "Food Poisoning",
            "treatment": "Fluids + charcoal",
            "score": 92
        })

    if diarrhea and temp > 39:
        results.append({
            "disease": "Bacterial Infection",
            "treatment": "Antibiotics + hydration",
            "score": 94
        })

    return results


# ===============================
# FALLBACK LOGIC
# ===============================
def fallback_diagnosis(data):

    vomiting = safe_int(data.get("vomiting"))
    diarrhea = safe_int(data.get("diarrhea"))
    coughing = safe_int(data.get("coughing"))
    skin = safe_int(data.get("skin"))
    weight = safe_int(data.get("weight"))

    symptom_count = vomiting + diarrhea + coughing + skin + weight

    if symptom_count == 0:
        return {
            "disease": "Healthy",
            "treatment": "No treatment required",
            "confidence": 95,
            "severity": "Low"
        }

    return {
        "disease": "General Checkup Needed",
        "treatment": "Consult a veterinarian",
        "confidence": 60,
        "severity": "Low"
    }


# ===============================
# MAIN DECISION FUNCTION
# ===============================
def decide_diagnosis(data):

    temp = safe_float(data.get("temp"))
    appetite = data.get("appetite", "Normal")

    # 🔍 DEBUG (optional)
    print("Received:", data)

    conditions = evaluate_conditions(data, temp, appetite)

    # If we found possible diseases
    if conditions:
        best = max(conditions, key=lambda x: x["score"])

        # Add slight randomness for realism
        confidence = best["score"] + random.randint(-5, 5)
        confidence = max(50, min(99, int(confidence)))

        if confidence > 90:
            severity = "High"
        elif confidence > 75:
            severity = "Medium"
        else:
            severity = "Low"

        return {
            "disease": best["disease"],
            "treatment": best["treatment"],
            "confidence": confidence,
            "severity": severity
        }

    # fallback
    return fallback_diagnosis(data)


# ===============================
# API ROUTE
# ===============================
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json or {}
    result = decide_diagnosis(data)
    return jsonify(result)


# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    app.run(debug=True)


  