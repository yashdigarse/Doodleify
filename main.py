import streamlit as st
from PIL import Image
import cv2
import numpy as np

def cartoonize_image(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply median blur
    gray = cv2.medianBlur(gray, 5)
    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    # Apply bilateral filter to smoothen the image
    color = cv2.bilateralFilter(img, 9, 300, 300)
    # Combine edges and color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

st.title("Pixar Style Image Converter")
st.write("Upload an image to convert it to Pixar style")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the uploaded image
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # Convert the image to Pixar style
    cartoon_image = cartoonize_image(img_array)
    
    # Display the original and cartoon images side by side
    st.image([img_array, cartoon_image], caption=['Original Image', 'Pixar Style Image'], use_column_width=True)
