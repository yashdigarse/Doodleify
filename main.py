import streamlit as st
from PIL import Image
import numpy as np

def pixelate_image(image, pixel_size):
    # Resize the image to simulate pixelation
    small_image = image.resize(
        (image.width // pixel_size, image.height // pixel_size),
        resample=Image.NEAREST
    )
    # Scale it back to original size
    pixelated_image = small_image.resize(
        (image.width, image.height),
        resample=Image.NEAREST
    )
    return pixelated_image

st.title("Minecraft Style Image Pixelator")
st.write("Convert your images into Minecraft-style pixel art!")

# Image upload
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Original Image", use_column_width=True)

    # Pixelation slider
    pixel_size = st.slider(
        "Select Pixelation Level (Block Size)",
        min_value=2,
        max_value=50,
        value=10,
    )

    # Apply pixelation
    pixelated_image = pixelate_image(image, pixel_size)

    # Display the result
    st.image(pixelated_image, caption="Minecraft Style Image", use_column_width=True)

    # Option to download
    pixelated_image.save("pixelated_image.png")
    with open("pixelated_image.png", "rb") as file:
        st.download_button(
            label="Download Pixelated Image",
            data=file,
            file_name="minecraft_pixelated.png",
            mime="image/png",
        )
