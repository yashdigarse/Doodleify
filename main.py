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
    doodle_image = cv2.addWeighted(gray_image, 0.7, inverted_edges, 0.3, 0)
    return doodle_image

def convert_to_pencil_sketch(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
    inverted_blurred = cv2.bitwise_not(blurred_image)
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    return pencil_sketch

def convert_to_sepia(image):
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_image = cv2.transform(image, sepia_filter)
    sepia_image = np.clip(sepia_image, 0, 255)
    return sepia_image

def convert_to_hdr(image):
    hdr_image = cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)
    return hdr_image

def convert_to_negative(image):
    negative_image = cv2.bitwise_not(image)
    return negative_image

def convert_to_emboss(image):
    kernel = np.array([[0, -1, -1],
                       [1, 0, -1],
                       [1, 1, 0]])
    emboss_image = cv2.filter2D(image, -1, kernel)
    return emboss_image

def convert_to_cartoon(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.medianBlur(gray_image, 5)
    edges = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color_image = cv2.bilateralFilter(image, 9, 300, 300)
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges)
    return cartoon_image

st.title("Photo Converter")


uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    effect = st.selectbox("Choose an effect", ["Doodle","Cartoon", "Pencil Sketch", "Sepia", "HDR", "Negative", "Emboss"])
    
    if effect == "Cartoon":
        output_image = convert_to_cartoon(image)
    elif effect == "Pencil Sketch":
        output_image = convert_to_pencil_sketch(image)
    elif effect == "Sepia":
        output_image = convert_to_sepia(image)
    elif effect == "HDR":
        output_image = convert_to_hdr(image)
    elif effect == "Negative":
        output_image = convert_to_negative(image)
    elif effect == "Emboss":
        output_image = convert_to_emboss(image)
    elif effect == "Doodle":
        output_image = convert_to_doodle(image)
    
    st.image(image, caption='Original Image', use_column_width=True)
    st.image(output_image, caption=f'{effect} Image', use_column_width=True)