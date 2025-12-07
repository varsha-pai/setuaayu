import json
import random
from datetime import datetime

def generate_bridge_data(scenario="normal", location_name=None):
    """
    Generates mock bridge sensor data.
    
    Args:
        scenario (str): "normal" or "critical". 
        location_name (str): Specific name of the bridge (optional).
    
    Returns:
        dict: Dictionary containing the sensor data. (Returning dict for easier usage, can be json dumped later or if user insisted on JSON object, I can return dict which is JSON-compatible in python or string)
        User said "returns a JSON object". In Python, that usually means a dict (which maps to JSON object) or a JSON string.
        I will return a dict as it is more pythonic for the app to consume, but if strict requirement is JSON, I'll return dict and let app verify.
        Actually, let's return a dict, and the app can jsonify it if needed, or I can return a json string.
        The prompt says "returns a JSON object". I will return a dict, as `client.chat.completions` usually takes string or dict.
        Let's look at the requirements: "Simulate keys...".
        I'll return a Python dictionary, which is the standard representation of a JSON object in Python code.
    """
    timestamp = datetime.now().isoformat()
    
    locations = [
        "Silk Board Junction Flyover",
        "Hebbal Flyover Service Rd",
        "KR Puram Suspension Bridge",
        "Domlur Flyover",
        "Yeshwanthpur Railway Overbridge",
        "Madiwala Underpass"
    ]
    location = location_name if location_name else random.choice(locations)
    
    # Stress (MPa) = Strain (microstrain) * Young's Modulus (GPa) / 1000 approx
    # Concrete E ~ 30 GPa. Steel E ~ 200 GPa. Let's assume Reinforced Concrete ~ 30-50 effective.
    # We will use simplified logic: Stress = Strain * 0.03 (approx)
    
    if scenario == "critical":
        # Critical values: high vibration, high strain, potential tilt
        vibration_x = round(random.uniform(0.31, 0.8), 4) # > 0.3g
        vibration_y = round(random.uniform(0.31, 0.8), 4)
        vibration_z = round(random.uniform(0.31, 0.8), 4)
        strain = round(random.uniform(500, 1000), 2) # High microstrain
        stress_mpa = round(strain * 0.035, 2)        # High stress
        tilt = round(random.uniform(2.0, 5.0), 2)     # Significant tilt
        health_score = random.randint(45, 65)         # Critical Health
        prediction_window = "45-60 days"
        defect_type = "Early-stage Rebar Corrosion"
        traffic_load = random.randint(4500, 8000)     # High Traffic (PCU/hr)
    else:
        # Normal values: low vibration, normal strain, negligible tilt
        vibration_x = round(random.uniform(0.001, 0.25), 4)
        vibration_y = round(random.uniform(0.001, 0.25), 4)
        vibration_z = round(random.uniform(0.001, 0.25), 4)
        strain = round(random.uniform(10, 100), 2)
        stress_mpa = round(strain * 0.030, 2)         # Normal stress
        tilt = round(random.uniform(-0.5, 0.5), 2)
        health_score = random.randint(95, 100)        # Optimal Health
        prediction_window = "None (Safe)"
        defect_type = "None"
        traffic_load = random.randint(800, 3500)      # Normal Traffic
        
    data = {
        "timestamp": timestamp,
        "location": location,
        "vibration_x": vibration_x,
        "vibration_y": vibration_y,
        "vibration_z": vibration_z,
        "strain": strain,
        "stress_mpa": stress_mpa,
        "tilt": tilt,
        "health_score": health_score,
        "prediction_window": prediction_window,
        "defect_type": defect_type,
        "traffic_load": traffic_load,
        "scenario": scenario
    }
    
    return data # Returning dict. If string is absolutely required, I'll change it.

if __name__ == "__main__":
    import json
    # Test the function
    print("Normal Scenario:", json.dumps(generate_bridge_data("normal"), indent=2))
    print("Critical Scenario:", json.dumps(generate_bridge_data("critical"), indent=2))
