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

# Custom CSS for aesthetics (as per instructions)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to right, #1a1a1a, #2d2d2d);
        color: #e0e0e0;
    }
    .metric-card {
        background-color: #333333;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff4b1f, #ff9068);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff9068, #ff4b1f);
        box-shadow: 0 0 15px rgba(255, 75, 31, 0.5);
    }
    h1 {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(0,0,0,0.5);
    }
    .stRadio > label {
        color: #ffffff;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🌉 SetuAayu: Bridge Safety Digital Twin")
st.markdown("### Real-time Structural Health Monitoring & AI Analysis")

# Sidebar
st.sidebar.header("Control Panel")
simulation_mode = st.sidebar.radio("Simulation Mode", ["Normal", "Critical"])

# Main Content - Live Metrics
st.markdown("---")
st.subheader("Live Sensor Telemetry")

# Generate Data
data_dict = generate_bridge_data(scenario=simulation_mode.lower())

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Vibration (g)</h3>
            <p style="font-size: 18px; color: {'#ff4b4b' if data_dict['vibration_x'] > 0.3 else '#00cc66'}">
                X: {data_dict['vibration_x']}<br>
                Y: {data_dict['vibration_y']}<br>
                Z: {data_dict['vibration_z']}
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Strain (µε)</h3>
            <p style="font-size: 32px; font-weight: bold; color: #3399ff">
                {data_dict['strain']}
            </p>
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

st.markdown("---")

# OpenAI Analysis Section
st.subheader("🤖 AI Safety Assessment")

if st.button("Run AI Analysis"):
    st.write("Analysis requested...")
    with st.spinner("Analyzing structural integrity..."):
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            # Mock Response
            time.sleep(1.5) # Simulate delay
            st.success("Analysis Complete (MOCK)")
            if simulation_mode == "Critical":
                st.error("**CRITICAL ALERT (Mock)**: High vibration and tilt detected above safety thresholds. Immediate inspection required.")
                st.write("**Detailed Insights:**")
                st.write("- Vibration levels > 0.3g indicate potential structural instability.")
                st.write("- Tilt deviation suggests foundation settlement.")
            else:
                st.success("**STATUS GREEN (Mock)**: All systems nominal. Structure operating within designed safety margins.")
            
            st.warning("Running in Demo Mode: No `OPENAI_API_KEY` found.")
            
        else:
            try:
                client = OpenAI(api_key=api_key)
                prompt = f"""
                Analyze the following bridge sensor data and provide a safety assessment.
                Data: {json.dumps(data_dict)}
                
                If values are high (Vibration > 0.3g, Tilt > 2 degrees), issue a critical warning.
                Otherwise, confirm safety. Keep it concise, professional, and actionable.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a structural engineering AI expert."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                analysis = response.choices[0].message.content
                st.success("Analysis Complete (AI-Powered)")
                st.write(analysis)
                
            except Exception as e:
                st.error(f"Error calling OpenAI API: {str(e)}")

# Add a footer
st.markdown("---")
st.caption("SetuAayu v1.0 | Hackathon Build | Built with Streamlit & OpenAI")
