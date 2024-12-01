import streamlit as st
from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO

# Load a pre-trained image-to-image model from Hugging Face
model = pipeline("image-to-image", model="CompVis/stable-diffusion-v1-4")

st.title('Image-to-Image Conversion with Hugging Face and Streamlit')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    # Convert the image using the model
    result = model(image)
    
    # Display the output image
    output_image = Image.open(BytesIO(result[0]["image"]))
    st.image(output_image, caption='Output Image.', use_column_width=True)