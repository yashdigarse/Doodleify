import streamlit as st
from PIL import Image
import cv2
import numpy as np
import tempfile

def cartoonize_image(img, ksize, sigma_color, sigma_space):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply median blur
    gray = cv2.medianBlur(gray, 5)
    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    # Apply bilateral filter to smoothen the image
    color = cv2.bilateralFilter(img, ksize, sigma_color, sigma_space)
    # Combine edges and color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

st.title("Advanced Pixar Style Image Converter")
st.write("Upload an image to convert it to Pixar style with adjustable settings")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the uploaded image
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    st.sidebar.title("Adjust Cartoon Effect")
    ksize = st.sidebar.slider("Kernel Size", 1, 15, 9, step=2)
    sigma_color = st.sidebar.slider("Sigma Color", 100, 500, 300)
    sigma_space = st.sidebar.slider("Sigma Space", 100, 500, 300)
    
    # Convert the image to Pixar style
    cartoon_image = cartoonize_image(img_array, ksize, sigma_color, sigma_space)
    
    # Display the original and cartoon images side by side
    st.image([img_array, cartoon_image], caption=['Original Image', 'Pixar Style Image'], use_column_width=True)
    
    # Provide a download button for the cartoon image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        cartoon_pil = Image.fromarray(cartoon_image)
        cartoon_pil.save(tmpfile.name)
        st.download_button(
            label="Download Pixar Style Image",
            data=tmpfile,
            file_name="pixar_style_image.png",
            mime="image/png"
        )
