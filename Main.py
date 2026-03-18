import streamlit as st
import os
import shutil

# 1. Folder Setup (Movies yaha save hongi)
SAVE_DIR = "my_library"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.set_page_config(page_title="Community OTT", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .stSidebar { background-color: #111111; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Our Shared Cinema")

# --- SIDEBAR: PERMANENT UPLOAD ---
st.sidebar.header("📤 Add to Public Library")
new_name = st.sidebar.text_input("Movie Name")
new_poster = st.sidebar.file_uploader("Upload Poster", type=["jpg", "png"])
new_video = st.sidebar.file_uploader("Upload MP4 Video", type=["mp4"])

if st.sidebar.button("Save Permanently"):
    if new_name and new_poster and new_video:
        # Movie ka folder banana
        movie_path = os.path.join(SAVE_DIR, new_name)
        if not os.path.exists(movie_path):
            os.makedirs(movie_path)
            
            # Saving Poster
            with open(os.path.join(movie_path, "poster.png"), "wb") as f:
                f.write(new_poster.getbuffer())
            
            # Saving Video
            with open(os.path.join(movie_path, "video.mp4"), "wb") as f:
                f.write(new_video.getbuffer())
                
            st.sidebar.success(f"'{new_name}' save ho gayi hai!")
            st.rerun() # Refresh to show new movie
        else:
            st.sidebar.error("Ye naam pehle se maujood hai.")

# --- MAIN INTERFACE: LOAD FROM FOLDER ---
all_movies = os.listdir(SAVE_DIR)

if not all_movies:
    st.info("Library khali hai. Sidebar se movies add karein.")
else:
    choice = st.selectbox("Select Movie", all_movies)
    
    col1, col2 = st.columns([1, 2.5])
    
    movie_folder = os.path.join(SAVE_DIR, choice)
    video_file = os.path.join(movie_folder, "video.mp4")
    poster_file = os.path.join(movie_folder, "poster.png")

    with col1:
        st.image(poster_file, use_container_width=True)
    
    with col2:
        st.subheader(f"Now Streaming: {choice}")
        st.video(video_file)

    # Gallery
    st.divider()
    st.write("### All Movies")
    cols = st.columns(6)
    for i, m in enumerate(all_movies):
        with cols[i % 6]:
            p_path = os.path.join(SAVE_DIR, m, "poster.png")
            st.image(p_path, caption=m)
  
