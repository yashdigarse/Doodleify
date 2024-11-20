import streamlit as st
from PIL import Image
import requests
import io

# Function to convert image to doodle using ClipDrop API
def convert_to_doodle(image, api_key):
    url = "https://clipdrop-api.co/sketch-to-image/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()
    
    response = requests.post(url, headers=headers, files={"file": image_bytes})
    if response.status_code == 200:
        doodle_image = Image.open(io.BytesIO(response.content))
        return doodle_image
    else:
        st.error("Failed to convert image to doodle.")
        return None

# Streamlit app
st.title("AI-based Doodle Image Converter")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Get API key from user input
    api_key = st.text_input("Enter your ClipDrop API key")

    if api_key:
        # Convert the image to doodle
        doodle_image = convert_to_doodle(image, api_key)

        if doodle_image:
            # Display the doodle image
            st.image(doodle_image, caption='Doodle Image', use_column_width=True)