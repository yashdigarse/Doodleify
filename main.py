import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from rembg import remove

def cartoonize(img):
    # Convert to grayscale and apply median blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    
    # Detect edges and threshold
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    # Apply bilateral filter for color smoothing
    color = cv2.bilateralFilter(img, 9, 300, 300)
    
    # Combine color image with edges
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    return cartoon

st.title("Image Cartoonifier")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)
    
    # Background removal
    remove_bg = st.checkbox("Remove Background")
    if remove_bg:
        bg_removed = remove(image)
        st.image(bg_removed, caption="Background Removed", use_column_width=True)
        image = bg_removed
    
    # Convert PIL Image to numpy array for OpenCV processing
    img_array = np.array(image)
    
    # Convert RGBA to RGB if necessary
    if img_array.shape[2] == 4:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    
    # Cartoonize
    cartoon = cartoonize(img_array)
    
    st.image(cartoon, caption="Cartoonized Image", use_column_width=True)
    
    # Convert the cartoonized image back to PIL Image for download
    cartoon_pil = Image.fromarray(cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB))
    
    # Create a BytesIO object for downloading
    buf = io.BytesIO()
    cartoon_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download Cartoonized Image",
        data=byte_im,
        file_name="cartoonized_image.png",
        mime="image/png"
    )

st.write("Note: This app uses OpenCV for cartoonization and rembg for background removal.")