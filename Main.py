import streamlit as st
import json
import os
import base64

# 1. Database Setup
DB_FILE = "cepflix_db.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Function to convert image to string (for permanent saving)
def image_to_base64(image_file):
    return base64.b64encode(image_file.getvalue()).decode()

# Page Config
st.set_page_config(page_title="CEPFLIX", layout="wide")

# Premium CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    h1 { color: #E50914; font-family: 'Arial Black'; font-size: 60px; }
    .stButton>button { background-color: #E50914; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #ff1e26; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>CEPFLIX</h1>", unsafe_allow_html=True)

# Load Data
if 'movies' not in st.session_state:
    st.session_state['movies'] = load_data()

# --- SIDEBAR: ADMIN ---
st.sidebar.title("🛠 Admin Panel")
auth = st.sidebar.text_input("Password", type="password")

if auth == "amrit":
    st.sidebar.success("Welcome, Amrit!")
    with st.sidebar.expander("Add New Movie", expanded=True):
        t = st.text_input("Movie Name")
        p = st.file_uploader("Upload Poster (Image)", type=["jpg", "png", "jpeg"])
        v = st.text_input("Video URL (Direct MP4 Link)")
        
        if st.button("Add to CEPFLIX"):
            if t and p and v:
                # Poster ko text mein badalna taaki save ho sake
                img_str = image_to_base64(p)
                new_movie = {"title": t, "poster": img_str, "video": v}
                
                st.session_state['movies'].append(new_movie)
                save_data(st.session_state['movies'])
                st.sidebar.success(f"'{t}' Saved Permanently!")
                st.rerun()
            else:
                st.sidebar.error("Bhai, sab kuch bharna zaruri hai!")

    if st.sidebar.button("Delete All"):
        save_data([])
        st.session_state['movies'] = []
        st.rerun()

# --- MAIN UI ---
if not st.session_state['movies']:
    st.info("👋 Welcome! Library khali hai. Sidebar se poster upload karein aur video link dalein.")
else:
    titles = [m['title'] for m in st.session_state['movies']]
    choice = st.selectbox("Search Movie:", titles)
    
    selected = next(m for m in st.session_state['movies'] if m['title'] == choice)
    
    st.divider()
    
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        # Displaying the uploaded poster
        st.image(f"data:image/png;base64,{selected['poster']}", width='stretch')
        st.subheader(selected['title'])
        
    with col2:
        st.video(selected['video'])
        st.caption(f"Streaming: {selected['title']}")

    # Gallery
    st.divider()
    st.subheader("Your Library")
    cols = st.columns(6)
    for i, m in enumerate(st.session_state['movies']):
        with cols[i % 6]:
            st.image(f"data:image/png;base64,{m['poster']}", caption=m['title'], width='stretch')
                
