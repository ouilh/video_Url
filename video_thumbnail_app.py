from pytube import YouTube
import requests
from PIL import Image
from io import BytesIO
import streamlit as st
from streamlit_option_menu import option_menu
import base64
import tempfile
import os

quality_mapping = {
    "1920x1080": 1920,
    "640x480": 640,
    "480x360": 480,
    "320x180": 320,
    "120x90": 120,
}
def get_thumbnail(video_url,h,v):
    try: 
        yt = YouTube(video_url)
        if yt:
            thumbnail_url = yt.thumbnail_url
            response = requests.get(thumbnail_url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((h, v), Image.ANTIALIAS)
            img.save("thumbnail.jpg", "JPEG")
            st.image(img, caption='Thumbnail')
            resized_image_bytesio = BytesIO()
            img.save(resized_image_bytesio, format='JPEG')
            # Add a download button
            st.download_button(
                label="Download Thumbnail",
                data=resized_image_bytesio,
                file_name='thumbnail.jpg',
                mime='image/jpeg'
            )
        else:
            st.error("Failed to capture the video frame.")
    except Exception as e:
        st.error("Failed to capture the video frame.")
# Example usage
# Streamlit App

with st.sidebar:
    selected= option_menu(
        menu_title="Main Menu",
        options=["Get Thumbnail", "Get Video", "Get audio","info"],
        icons=["image","play","speaker","info"],
    )
if selected == "Get Thumbnail":
    st.title("_Video :blue[Thumbnail] Extractor_")
    st.write("Enter a video URL to get its thumbnail")

    video_url = st.text_input("Video URL")
    quality = st.selectbox("Thumbnail Quality", ["1920x1080", "640x480", "480x360", "320x180", "120x90"])
    h=quality_mapping.get(quality)
    if h==1920 :
        v=1080
    elif h==640:
        v=480
    elif h==480:
        v=360
    elif h==320:
        v=180
    elif h==120:
        v=90
    if st.button("Get Thumbnail"):
        if video_url:
            st.success('Thumbnail', icon="✅")
            get_thumbnail(video_url,h,v)
            
            
        else:
            st.warning("Please enter a video URL.")

    st.write("Note: Make sure the video URL is accessible and public.")
if selected=="Get Video":
        
    

        # Streamlit app title
    st.title("YouTube Video Downloader")

    # Function to download YouTube video
    def download_video(youtube_url, selected_quality):
        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(res=selected_quality).first()
            if stream:
                st.text("Generating download link...")
                temp_dir = tempfile.mkdtemp()
                temp_file = os.path.join(temp_dir, f"{yt.title}.mp4")
                stream.download(output_path=temp_dir)
                st.success("Video downloaded successfully!")

                st.download_button(
                    label="Click here to download the video",
                    key='download',
                    data=temp_file,
                    on_click=None,
                )
            else:
                st.warning("No video available with the selected quality.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # User input: YouTube URL
    youtube_url = st.text_input("Enter YouTube Video URL:")

    # User input: Video quality
    selected_quality = st.selectbox(
        "Select Video Quality:",
        ["360p", "720p", "1080p"],
        index=1  # Default to 720p
    )

    # Download button
    if st.button("Download"):
        if youtube_url.strip() == "":
            st.warning("Please enter a valid YouTube URL.")
        else:
            download_video(youtube_url, selected_quality)

    # Information
    st.markdown("Note: This app only supports downloading videos with the selected quality.")