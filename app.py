import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Set up colors and fonts
primaryColor = "#FF5733"  # Orange
backgroundColor = "#1E1E1E"  # Dark Gray
textColor = "#FFFFFF"  # White
font = "sans serif"

# Load models and data
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# Set page configuration
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and header
st.title("Laptop Price Predictor")
st.markdown("---")

# Sidebar - User inputs
st.sidebar.header("User Inputs")
company = st.sidebar.selectbox('Brand', df['Company'].unique(), key='company')
type_name = st.sidebar.selectbox('Type', df['TypeName'].unique(), key='type')
ram = st.sidebar.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64], key='ram')
weight = st.sidebar.number_input('Weight of Laptop', key='weight')
touchscreen = st.sidebar.selectbox('Touchscreen', ['NO', 'YES'], key='touchscreen')
ips = st.sidebar.selectbox('IPS', ['NO', 'YES'], key='ips')
screen_size = st.sidebar.number_input('Screen Size (in inches)', key='screen_size')
resolution = st.sidebar.selectbox("Resolution", ['1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800', '2560x1600', '2560x1440', '2304x1440'], key='resolution')
cpu = st.sidebar.selectbox('CPU Brand', df['Cpu_brand'].unique(), key='cpu')
hdd = st.sidebar.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048], key='hdd')
SSD = st.sidebar.selectbox('SSD (in GB)', [0, 128, 256, 512, 1024], key='ssd')
gpu = st.sidebar.selectbox('GPU Brand', df['Gpu brand'].unique(), key='gpu')
os = st.sidebar.selectbox('Operating System', df['os'].unique(), key='os')

# Predict price button
if st.sidebar.button('Predict Price'):
    ppi = None
    if touchscreen == 'YES':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'YES':
        ips = 1
    else:
        ips = 0

    X_res = int(resolution.split('x')[0])
    y_res = int(resolution.split('x')[1])
    if screen_size != 0:
        ppi = ((X_res ** 2) + (y_res ** 2)) ** 0.5 / screen_size
    else:
        st.warning("Screen size cannot be zero. Please provide a valid screen size.")
        ppi = None
    query = np.array([company, type_name, ram, weight, touchscreen, ips, ppi, cpu, hdd, SSD, gpu, os])
    query = query.reshape(1, 12)
    predicted_price = int(np.exp(pipe.predict(query)))
    st.sidebar.success(f"Predicted Price: ${predicted_price}")

# Footer
st.markdown("---")
st.write("Made with ❤️ by [zeel makwana]")
