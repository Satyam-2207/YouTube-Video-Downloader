import streamlit as st
import subprocess
import yt_dlp

# Page config for title and icon
st.set_page_config(page_title="YouTube Downloader", layout="centered")

# CSS to prevent button text wrapping and add bold style
st.markdown(
    """
    <style>
    .stButton > button {
        white-space: nowrap;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Logo at the top
st.image("https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg", width=150)

# Header and subtitle
st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>YouTube Video Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555; font-size:18px;'>Download videos or audio in your preferred quality</p>", unsafe_allow_html=True)
st.markdown("---")

# Input columns for URL and quality select
col1, col2 = st.columns([4, 3])

with col1:
    url = st.text_input("Enter YouTube URL", placeholder="https://youtube.com/...")
with col2:
    quality = st.selectbox(
        "Choose quality & format",
        ("360p", "480p", "720p", "1080p", "MP3 only (audio)", "MP4 only (video+audio)")
    )

# Optional filename input
filename = st.text_input("Optional: Set output filename (without extension)")

# Show video info if URL is given and valid
if url:
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            st.markdown(f"**Title:** {info.get('title', 'N/A')}")
            duration = info.get('duration')
            if duration:
                mins = duration // 60
                secs = duration % 60
                st.markdown(f"**Duration:** {mins} min {secs} sec")
            filesize = info.get('filesize') or info.get('filesize_approx')
            if filesize:
                size_mb = filesize / (1024 * 1024)
                st.markdown(f"**Approximate Size:** {size_mb:.2f} MB")
    except Exception as e:
        st.warning("Unable to fetch video info. Please check the URL.")

# Center the download button with proper width
col_left, col_center, col_right = st.columns([3, 2, 3])
with col_center:
    download_clicked = st.button("Download", use_container_width=True)

# Function to get yt-dlp format code based on quality selection
def get_format_code(quality):
    if quality == "360p":
        return "bestvideo[height=360]+bestaudio"
    elif quality == "480p":
        return "bestvideo[height=480]+bestaudio"
    elif quality == "720p":
        return "bestvideo[height=720]+bestaudio"
    elif quality == "1080p":
        return "bestvideo[height=1080]+bestaudio"
    elif quality == "MP3 only (audio)":
        return "bestaudio[ext=m4a]"
    elif quality == "MP4 only (video+audio)":
        return "bestvideo+bestaudio"
    else:
        return "bestvideo+bestaudio"

# Initialize download history in session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Handle download logic
if download_clicked:
    if url:
        st.info(f"Starting download in **{quality}** quality...")

        format_code = get_format_code(quality)

        cmd = [
            "yt-dlp",
            "-f", format_code,
            "--merge-output-format", "mp4",
            url
        ]

        if filename.strip():
            cmd += ["-o", filename.strip() + ".%(ext)s"]

        if quality == "MP3 only (audio)":
            cmd += ["-x", "--audio-format", "mp3"]

        with st.spinner("Downloading... Please wait."):
            result = subprocess.run(cmd, capture_output=True, text=True)

        st.text_area("Download Log:", value=result.stdout if result.stdout else result.stderr, height=200)

        if result.returncode == 0:
            st.success("Download completed successfully.")
            # Add URL to download history
            st.session_state.history.append(url)
        else:
            st.error("Download failed. Please check the URL or try again.")
    else:
        st.warning("Please enter a valid YouTube URL.")

# Show download history if any
if st.session_state.history:
    st.markdown("---")
    st.markdown("### Download History")
    for i, u in enumerate(st.session_state.history[::-1], 1):
        st.write(f"{i}. {u}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:#999; font-size:12px;'>Created by @satyamparida</p>", unsafe_allow_html=True)
