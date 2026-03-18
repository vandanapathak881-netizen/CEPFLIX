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
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def image_to_base64(image_file):
    return base64.b64encode(image_file.getvalue()).decode()

# Page Config
st.set_page_config(page_title="CEPFLIX", layout="wide")

# Premium CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    h1 { color: #E50914; font-family: 'Arial Black'; font-size: 60px; margin-bottom: 0px; }
    .stButton>button { background-color: #E50914; color: white; border: none; font-weight: bold; border-radius: 4px; }
    .stButton>button:hover { background-color: #ff1e26; }
    /* Delete button style */
    div.stButton > button:first-child[style*="background-color: rgb(255, 75, 75)"] {
        background-color: #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>CEPFLIX</h1>", unsafe_allow_html=True)
st.caption("Admin Controlled Streaming Platform")

# Load Data
if 'movies' not in st.session_state:
    st.session_state['movies'] = load_data()

# --- SIDEBAR: ADMIN PANEL ---
st.sidebar.title("🛠 Admin Panel")
auth = st.sidebar.text_input("Password", type="password")

if auth == "amrit":
    st.sidebar.success("Welcome, Amrit!")
    
    # ADD SECTION
    with st.sidebar.expander("➕ Add New Movie", expanded=False):
        t = st.text_input("Movie Name")
        p = st.file_uploader("Upload Poster", type=["jpg", "png", "jpeg"])
        v = st.text_input("Video URL (MP4 Link)")
        
        if st.button("Publish Movie"):
            if t and p and v:
                img_str = image_to_base64(p)
                new_movie = {"title": t, "poster": img_str, "video": v}
                st.session_state['movies'].append(new_movie)
                save_data(st.session_state['movies'])
                st.sidebar.success(f"Added: {t}")
                st.rerun()
            else:
                st.sidebar.error("Sari details bhariye!")

    # DELETE SECTION
    if st.session_state['movies']:
        with st.sidebar.expander("🗑 Manage / Delete Movies", expanded=True):
            movie_titles = [m['title'] for m in st.session_state['movies']]
            to_delete = st.selectbox("Select Movie to Remove", movie_titles)
            
            if st.sidebar.button(f"Delete '{to_delete}'"):
                # Movie list se hatana
                st.session_state['movies'] = [m for m in st.session_state['movies'] if m['title'] != to_delete]
                save_data(st.session_state['movies'])
                st.sidebar.warning(f"Deleted: {to_delete}")
                st.rerun()
    
    if st.sidebar.button("Clear Full Library"):
        if st.sidebar.checkbox("Confirm Reset?"):
            save_data([])
            st.session_state['movies'] = []
            st.rerun()
else:
    st.sidebar.info("Enter password 'amrit' to manage.")

# --- MAIN UI ---
if not st.session_state['movies']:
    st.info("👋 Welcome! Library khali hai. Admin panel se movies add karein.")
else:
    all_titles = [m['title'] for m in st.session_state['movies']]
    choice = st.selectbox("Search Movie:", all_titles)
    
    selected = next(m for m in st.session_state['movies'] if m['title'] == choice)
    
    st.divider()
    
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        st.image(f"data:image/png;base64,{selected['poster']}", width='stretch')
        st.subheader(selected['title'])
        
    with col2:
        st.video(selected['video'])

    # Collection Gallery
    st.divider()
    st.subheader("Your Collection")
    cols = st.columns(6)
    for i, m in enumerate(st.session_state['movies']):
        with cols[i % 6]:
            st.image(f"data:image/png;base64,{m['poster']}", caption=m['title'], width='stretch')
            
