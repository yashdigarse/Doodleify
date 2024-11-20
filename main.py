import streamlit as st
import cv2
import numpy as np
from PIL import Image

def convert_to_doodle(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Edge detection
    edges = cv2.Canny(gray_image, 100, 200)
    # Invert edges
    inverted_edges = cv2.bitwise_not(edges)
    # Blend the original grayscale image with the inverted edges
    doodle_image = cv2.addWeighted(gray_image, 0.5, inverted_edges, 0.5, 0)
    return doodle_image

st.title("Photo to Doodle Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Convert the image to doodle
    doodle_image = convert_to_doodle(image)
    
    # Display the original and doodle images
    st.image(image, caption='Original Image', use_column_width=True)
    st.image(doodle_image, caption='Doodle Image', use_column_width=True)
