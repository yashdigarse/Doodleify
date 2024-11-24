import streamlit as st
import cv2
import numpy as np
from PIL import Image
from transformers import pipeline

# Load the pre-trained model
model = pipeline("image-to-image", model="CompVis/stable-diffusion-v1-4")

def cartoonify_image(image):
    # Convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Use the model to generate a cartoon version
    cartoon = model(image)
    return cartoon

st.title("AI Cartoonify Your Image!")
st.write("Upload an image to cartoonify it using AI.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = np.array(Image.open(uploaded_file))
    cartoon = cartoonify_image(image)
    st.image(cartoon, caption='Cartoonified Image', use_column_width=True)