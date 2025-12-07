import streamlit as st
import pandas as pd
import time
import os
import json
from openai import OpenAI
from bridge_sim import generate_bridge_data

# Page Config
st.set_page_config(
    page_title="SetuAayu - Bridge Digital Twin",
    page_icon="🌉",
    layout="wide"
)

import streamlit.components.v1 as components

def get_bridge_viewer_html(data):
    try:
        with open("bridge_viewer_template.html", "r") as f:
            html_template = f.read()
    except FileNotFoundError:
        return "<div>Template not found</div>"
    
    # Simple template injection
    html_content = html_template.replace("{{VIB_X}}", str(data['vibration_x']))\
                                .replace("{{VIB_Y}}", str(data['vibration_y']))\
                                .replace("{{VIB_Z}}", str(data['vibration_z']))\
                                .replace("{{STRESS}}", str(data['strain']))\
                                .replace("{{TILT}}", str(data['tilt']))
    return html_content

# Custom CSS for aesthetics (as per instructions)
st.markdown("""
<style>
    /* Global Reset & Sci-Fi Font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;400&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: #e0e0e0;
        font-family: 'Roboto', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Glassmorphism Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00d2ff;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 30px;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #3a7bd5, #00d2ff);
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.6);
        transform: scale(1.05);
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0c1219;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Neon Text Effects */
    .highlight-red { color: #ff0f7b; text-shadow: 0 0 10px rgba(255, 15, 123, 0.7); }
    .highlight-green { color: #00f260; text-shadow: 0 0 10px rgba(0, 242, 96, 0.7); }
    .highlight-blue { color: #0575E6; text-shadow: 0 0 10px rgba(5, 117, 230, 0.7); }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🌉 SetuAayu: Bridge Safety Digital Twin")
st.markdown("### Real-time Structural Health Monitoring & AI Analysis")

# Sidebar
st.sidebar.header("Control Panel")

# --- Asset Onboarding (Image to 3D) ---
uploaded_file = st.sidebar.file_uploader("Upload Architecture / Bridge Image", type=['jpg', 'png', 'jpeg'])
model_ready = False

if uploaded_file is not None:
    st.sidebar.image(uploaded_file, caption="Source Image", use_container_width=True)
    
    if "reconstruction_done" not in st.session_state:
        # Simulation of complex 3D reconstruction
        progress_text = "Initializing Photogrammetry Engine..."
        my_bar = st.sidebar.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.03) # Simulation delay
            if percent_complete < 30:
                my_bar.progress(percent_complete + 1, text="Initializing Photogrammetry Engine...")
            elif percent_complete < 60:
                my_bar.progress(percent_complete + 1, text="Generating Point Cloud...")
            else:
                my_bar.progress(percent_complete + 1, text="Meshing 3D Surface...")
            
        time.sleep(0.5)
        my_bar.empty()
        st.session_state["reconstruction_done"] = True
    
    st.sidebar.success("✅ 3D Model Generated from Image")
    model_ready = True
else:
    st.sidebar.info("Upload an image to generate a Digital Twin.")

simulation_mode = st.sidebar.radio("Simulation Mode", ["Normal", "Critical"])

# --- Location Selector ---
# Define locations list here or import it (defining here for simplicity and UI control)
blr_locations = [
    "Silk Board Junction Flyover",
    "Hebbal Flyover Service Rd",
    "KR Puram Suspension Bridge",
    "Domlur Flyover",
    "Yeshwanthpur Railway Overbridge",
    "Madiwala Underpass"
]

# Real-world images for "Web Scraping" simulation
bridge_images = {
    "Silk Board Junction Flyover": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Silk_board_junction.jpg/1024px-Silk_board_junction.jpg",
    "Hebbal Flyover Service Rd": "https://upload.wikimedia.org/wikipedia/commons/4/42/Hebbal_Flyover_Bangalore.jpg",
    "KR Puram Suspension Bridge": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/K_R_Puram_Bridge.jpg/1200px-K_R_Puram_Bridge.jpg",
    "Domlur Flyover": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Domlur_Flyover.jpg",
    "Yeshwanthpur Railway Overbridge": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/498114811.jpg?k=20f5c184478144214f4e38e670404439c28929ac747445c73860070119293673&o=&hp=1",
    "Madiwala Underpass": "https://content.jdmagicbox.com/comp/bangalore/48/080p5005948/catalogue/madiwala-underpass-madiwala-bangalore-bridge-construction-contractors-3p9f5.jpg"
}

selected_location = st.sidebar.selectbox("Select Bridge Location", blr_locations)

# --- Web Scraping & Twin Generation Module ---
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Digital Twin Generator")
scrape_btn = st.sidebar.button("🔍 Scrape Web & Reconstruct")

scraped_image_url = None

if scrape_btn:
    with st.sidebar.status("Running OSINT Crawlers...", expanded=True) as status:
        st.write("🕷️ Spawning bots on Google Images...")
        time.sleep(1)
        st.write(f"📂 Found 14 historical images for '{selected_location}'")
        time.sleep(0.8)
        st.write("📐 Triangulating Photogrammetry Points...")
        time.sleep(1.2)
        st.write("🧊 Constructing 3D Mesh...")
        status.update(label="✅ Digital Twin Ready", state="complete", expanded=False)
    
    st.session_state['scraped_active'] = True
    st.sidebar.success("Twin Synced with Live Data")
    
if st.session_state.get('scraped_active'):
    # Show the "Scraped" image
    st.sidebar.image(bridge_images.get(selected_location, "https://via.placeholder.com/300"), caption=f"Reference: {selected_location}", use_container_width=True)
    scraped_image_url = bridge_images.get(selected_location)
    model_ready = True # Enable the Twin view

# Main Content - Live Metrics
st.markdown("---")
# Header with Location
st.subheader(f"📍 Live Sensor Telemetry: {selected_location}")
st.caption(f"Asset ID: {'TWIN-GEN-001' if st.session_state.get('scraped_active') else 'BLR-CIVIC-8842'} | Monitoring Node: Active")

# Generate Data
data_dict = generate_bridge_data(scenario=simulation_mode.lower(), location_name=selected_location) 

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Vibration (g)</h3>
            <p style="font-size: 18px; color: {'#ff4b4b' if data_dict['vibration_x'] > 0.3 else '#00cc66'}">
                x: {data_dict['vibration_x']}<br>
                y: {data_dict['vibration_y']}<br>
                z: {data_dict['vibration_z']}
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Stress (MPa)</h3>
            <p style="font-size: 32px; font-weight: bold; color: #3399ff">
                {data_dict['stress_mpa']}
            </p>
            <span style="font-size:12px; color:#888">Legacy Strain: {data_dict['strain']}µε</span>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Tilt (°)</h3>
            <p style="font-size: 32px; font-weight: bold; color: {'#ff4b4b' if abs(data_dict['tilt']) > 2.0 else '#00cc66'}">
                {data_dict['tilt']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
with col4:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Traffic (PCU/hr)</h3>
            <p style="font-size: 32px; font-weight: bold; color: {'#ff4b4b' if data_dict['traffic_load'] > 4000 else '#ffa500'}">
                {data_dict['traffic_load']}
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- Structural Health Score ---
st.markdown("### 🏥 Structural Health Score")
health_color = "#00cc66" # Green
if data_dict['health_score'] < 70: health_color = "#ff4b4b" # Red
elif data_dict['health_score'] < 90: health_color = "#ffa500" # Orange

st.markdown(f"""
    <div style="background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; text-align: center; border: 2px solid {health_color}; margin-bottom: 20px;">
        <h2 style="color: #e0e0e0; margin: 0;">OVERALL ASSET HEALTH</h2>
        <h1 style="font-size: 80px; margin: 0; color: {health_color}; text-shadow: 0 0 20px {health_color};">
            {data_dict['health_score']}%
        </h1>
        <p style="color: #aaa;">Predicted Failure Window: <span style="color: #fff; font-weight: bold;">{data_dict['prediction_window']}</span></p>
    </div>
""", unsafe_allow_html=True)

col_twin, col_drone = st.columns([2, 1])

with col_twin:
    # --- 3D Digital Twin Visualizer ---
    st.markdown(f"### 🧊 3D Digital Twin ({'Custom Model' if model_ready else 'Live IoT'})")
    html_3d = get_bridge_viewer_html(data_dict)
    components.html(html_3d, height=450)
    
with col_drone:
    # --- Drone Scan / Upload Visuals ---
    st.markdown("### � Visual Inspection Input")
    
    # Priority: Uploaded File > Location Image > Default Placeholder
    display_img = "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?q=80&w=600&auto=format&fit=crop"
    caption_text = "LiDAR Depth Map - Default"
    
    # Check if we have a specific image for this location
    location_img_url = bridge_images.get(selected_location)

    if model_ready and uploaded_file is not None:
        display_img = uploaded_file
        caption_text = f"User Upload: {uploaded_file.name}"
        st.info(f"Analyzing: {uploaded_file.name}")
    elif location_img_url:
        display_img = location_img_url
        caption_text = f"Asset Reference: {selected_location}"
        # Only show analyzing text if we are 'analyzing' (simulated)
        if st.session_state.get('scraped_active'):
             st.info(f"Analyzing Web Data for: {selected_location}")
        
    st.image(display_img, caption=caption_text, use_container_width=True)

    if simulation_mode == "Critical":
        st.error(f"⚠️ Vision AI: Structural Defects Detected ({data_dict['defect_type']})")
    else:
        st.success("✅ Vision AI: No Surface Defects Found")

st.markdown("---")

from datetime import datetime
# --- REPORT GENERATION ---
if st.button("📄 Generate Safety Audit Report"):
    with st.spinner("Compiling Engineering Report..."):
        time.sleep(1.5)
        
        report_text = f"""
        # 🌉 SetuAayu STRUCTURAL SAFETY AUDIT REPORT
        **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        **Asset:** {selected_location}
        **Asset ID:** BLR-CIVIC-8842-TWIN
        
        ---
        ## 1. TELEMETRY SUMMARY
        - **Vibration:** {data_dict['vibration_x']}g (Max Axis)
        - **Stress Load:** {data_dict['stress_mpa']} MPa
        - **Traffic Volume:** {data_dict['traffic_load']} PCU/hr
        
        ## 2. AI SAFETY ASSESSMENT
        - **Health Score:** {data_dict['health_score']}/100
        - **Condition:** {'CRITICAL' if data_dict['health_score'] < 70 else 'OPTIMAL'}
        - **Predicted Failure Window:** {data_dict['prediction_window']}
        
        ## 3. FUTURE CONDITION PREDICTION (AI PROJECTION)
        Based on current stress accumulation of {data_dict['stress_mpa']} MPa/hr and traffic patterns:
        - **3 Months:** {'Micro-fissures likely in Sector 4' if data_dict['health_score'] < 80 else 'No significant degradation expected.'}
        - **1 Year:** {'Major rehabilitation required.' if data_dict['health_score'] < 60 else 'Routine maintenance sufficient.'}
        
        ## 4. RECOMMENDATIONS
        1. {'Reduce traffic load immediately' if data_dict['traffic_load'] > 5000 else 'Maintain current traffic flow.'}
        2. {'Schedule NDT (Non-Destructive Testing) this week' if data_dict['health_score'] < 70 else 'Next inspection due in 6 months.'}
        
        *Generated by SetuAayu AI Engine v1.0*
        """
        
        st.text_area("Report Preview", report_text, height=400)
        st.download_button("Download Report (PDF)", report_text, file_name=f"Report_{selected_location.replace(' ', '_')}.txt")

import pickle
import numpy as np

# Load ML Model
try:
    with open("model.pkl", "rb") as f:
        ml_model = pickle.load(f)
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# ... [Previous imports mostly ok, just ensuring location] ...
from openai import OpenAI
from bridge_sim import generate_bridge_data

# [Skipping to Analysis Section logic substitution]

if st.button("Run AI Analysis"):
    st.write("Analysis requested...")
    with st.spinner("Analyzing structural integrity..."):
        api_key = os.environ.get("OPENAI_API_KEY")
        
        # Priority 1: OpenAI (if key exists)
        if api_key:
             # ... [Keep existing OpenAI logic] ...
             pass
        
        # Priority 2: Trained ML Model (if file exists and no API key)
        elif model_loaded:
            time.sleep(1.0) # UX delay
            
            # Prepare Input Vector
            input_data = np.array([[
                data_dict['vibration_x'],
                data_dict['vibration_y'], 
                data_dict['vibration_z'],
                data_dict['strain'],
                data_dict['tilt']
            ]])
            
            # Predict
            prediction = ml_model.predict(input_data)[0] # 0 = Normal, 1 = Critical
            probs = ml_model.predict_proba(input_data)[0]
            confidence = max(probs) * 100
            
            st.success(f"Analysis Complete (Random Forest Model | Confidence: {confidence:.2f}%)")
            
            if prediction == 1: # Critical
                st.error(f"**CRITICAL ALERT**: ML Model detected structural instability.")
                st.markdown("#### Diagnostics (Model Feature Importance):")
                st.markdown(f"- **Vibration Impact**: High (Contributing to {probs[1]*100:.1f}% risk score)")
                st.markdown(f"- **Strain Load**: {data_dict['strain']}µε")
                
                st.markdown("#### Recommended Actions:")
                st.warning("1. Immediate restriction of heavy vehicle traffic.\n2. Deploy drone for visual crack inspection.")
            else:
                st.success(f"**STATUS OPTIMAL**: ML Model predicts safe operations.")
                st.info(f"Probability of Failure: {probs[1]*100:.2f}% (Negligible)")
                
            st.caption("Running in 'ML Inference' Mode: Using local `model.pkl` trained on `bridge_data.csv`.")

        # Priority 3: Rule-Based Fallback (if no model and no API key)
        else:
             # ... [Keep fallback rule logic] ...
            st.warning("Model not found. Falling back to Rule-Based Engine.")
            vib_max = max(data_dict['vibration_x'], data_dict['vibration_y'], data_dict['vibration_z'])
            # [Existing logic follows...]

# Add a footer
st.markdown("---")
st.caption("SetuAayu v1.0 | Hackathon Build | Built with Streamlit & OpenAI")
