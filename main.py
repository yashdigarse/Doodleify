import streamlit as st
import cv2
import numpy as np
from PIL import Image

def remove_background(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply a binary threshold to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Create a mask with the same dimensions as the image
    mask = np.zeros_like(image)
    # Draw the contours on the mask
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)
    # Bitwise-and to get the foreground
    foreground = cv2.bitwise_and(image, mask)
    return foreground, mask

def convert_to_doodle(image):
    # Remove background
    foreground, mask = remove_background(image)
    # Convert to grayscale
    gray_image = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise and detail
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # Edge detection using Canny
    edges = cv2.Canny(blurred_image, 50, 150)
    # Dilate edges to make them more pronounced
    dilated_edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    # Invert edges
    inverted_edges = cv2.bitwise_not(dilated_edges)
    # Blend the original grayscale image with the inverted edges
    doodle_image = cv2.bitwise_and(gray_image, gray_image, mask=inverted_edges)
    # Convert doodle image to 3 channels
    doodle_image = cv2.cvtColor(doodle_image, cv2.COLOR_GRAY2BGR)
    # Ensure the mask is a single channel
    single_channel_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # Add a new background (white background in this case)
    new_background = np.ones_like(image) * 255
    # Combine the doodle foreground with the new background
    combined_image = cv2.bitwise_and(new_background, new_background, mask=cv2.bitwise_not(single_channel_mask))
    combined_image = cv2.add(combined_image, doodle_image)
    return combined_image

st.title("Photo to Doodle Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Convert the image to doodle
    doodle_image = convert_to_doodle(image)
    
    # Display the original and doodle images
    st.image(image, caption='Original Image', use_column_width=True)
    st.image(doodle_image, caption='Doodle Image', use_column_width=True)