import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime

# Set page config to minimize Streamlit interference
st.set_page_config(
    page_title="OSINT Toolkit - Pre-Launch",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS to remove Streamlit artifacts and match HTML
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #2a2a2a, #4a4a4a);
            padding: 0;
            margin: 0;
            overflow: hidden;
            height: 100vh;
        }
        .css-1aumxhk, .css-1y0tads, .css-1d391kg {
            padding: 0 !important;
            margin: 0 !important;
        }
        .css-1v0mbdj {
            display: none; /* Hide footer */
        }
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define launch date
launch_date = datetime(2025, 7, 26, 10, 0, 0, tzinfo=None)  # 10:00 AM IST, July 26, 2025
current_time = datetime.now()

# Redirect to GitHub page if launch date has passed
if current_time >= launch_date:
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url=https://krishna7124.github.io/osintframework/">
    """, unsafe_allow_html=True)
else:
    # Load and render the HTML file
    html_file_path = os.path.join(os.path.dirname(__file__), "index1.html")
    if os.path.exists(html_file_path):
        with open(html_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    else:
        html_content = """
        <h1>Error</h1>
        <p>Index1.html not found. Please ensure the file is in the same directory as this script.</p>
        """

    components.html(
        html_content,
        height=800,  # Matches the content height from your design
        scrolling=False,
    )