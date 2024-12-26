import streamlit as st
import urllib.request
import json
import re

def fetch_loom_download_url(video_id):
    """Fetch the download URL for a Loom video."""
    try:
        request = urllib.request.Request(
            url=f"https://www.loom.com/api/campaigns/sessions/{video_id}/transcoded-url",
            headers={},
            method="POST",
        )
        response = urllib.request.urlopen(request)
        body = response.read()
        content = json.loads(body.decode("utf-8"))
        return content["url"]
    except Exception as e:
        st.error(f"Failed to fetch video URL: {e}")
        return None

def fetch_video_name(video_id):
    """Fetch the video name based on the Loom video metadata."""
    try:
        request = urllib.request.Request(
            url=f"https://www.loom.com/api/campaigns/sessions/{video_id}",
            headers={},
            method="GET",
        )
        response = urllib.request.urlopen(request)
        body = response.read()
        content = json.loads(body.decode("utf-8"))
        return re.sub(r'[\\/*?\"<>|]', "_", content.get("name", "loom_video"))  # Sanitize filename
    except Exception as e:
        pass
        return "loom_video"

def main():
    st.title("Loom Video Downloader")

    # Input URL
    video_url = st.text_input(
        "Enter the Loom video URL:", placeholder="https://www.loom.com/share/[ID]"
    )

    if video_url:
        # Extract video ID
        video_id = video_url.split("/")[-1]

        # Fetch video name and download URL
        with st.spinner("Fetching video details..."):
            download_url = fetch_loom_download_url(video_id)
            video_name = fetch_video_name(video_id)

        if download_url:
            # Download the video as a binary file
            with st.spinner("Preparing download..."):
                try:
                    response = urllib.request.urlopen(download_url)
                    video_data = response.read()

                    # Provide file download button
                    st.success("Video is ready to download!")
                    st.download_button(
                        label="Download Video",
                        data=video_data,
                        file_name=f"{video_name}.mp4",
                        mime="video/mp4",
                    )
                except Exception as e:
                    st.error(f"Failed to download the video: {e}")

if __name__ == "__main__":
    main()
