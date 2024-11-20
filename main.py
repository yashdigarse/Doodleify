import streamlit as st
from PIL import Image
import requests
import io

# Function to convert image to sketch using LightX API
def convert_to_sketch(image, api_key):
    url = "https://api.lightxeditor.com/photo-to-sketch"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()
    
    response = requests.post(url, headers=headers, files={"file": ("image.png", image_bytes, "image/png")})
    
    if response.status_code == 200:
        sketch_image = Image.open(io.BytesIO(response.content))
        return sketch_image
    else:
        st.error(f"Failed to convert image to sketch. Error: {response.json().get('error', 'Unknown error')}")
        return None

# Streamlit app
st.title("AI-based Sketch Image Converter")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Get API key from user input
    api_key = st.text_input("Enter your LightX API key")

    if api_key:
        # Convert the image to sketch
        sketch_image = convert_to_sketch(image, api_key)

        if sketch_image:
            # Display the sketch image
            st.image(sketch_image, caption='Sketch Image', use_column_width=True)