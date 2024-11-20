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


def convert_to_cartoon(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply median blur
    gray_image = cv2.medianBlur(gray_image, 5)
    # Edge detection
    edges = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    # Convert back to color
    color_image = cv2.bilateralFilter(image, 9, 300, 300)
    # Combine edges with the color image
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges)
    return cartoon_image


st.title("Photo to Doodle Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Convert the image to doodle
    doodle_image = convert_to_doodle(image)

    # Convert the image to cartoon
    cartoon_image = convert_to_cartoon(image)

    
    # Display the original and doodle images
    st.image(image, caption='Original Image', use_column_width=True)
    st.image(cartoon_image, caption='Cartoon Image', use_column_width=True)
    
    st.image(doodle_image, caption='Doodle Image', use_column_width=True)
