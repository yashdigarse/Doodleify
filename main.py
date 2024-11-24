import streamlit as st
from PIL import Image

def convert_to_minecraft_style(image, size=(16, 16)):
    # Resize the image to 16x16
    image = image.resize(size, Image.Resampling.NEAREST)
    # Scale it back up for better visibility
    return image.resize((size[0] * 20, size[1] * 20), Image.Resampling.NEAREST)

st.title("Minecraft 16x16 Character Converter")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    # Convert to Minecraft style
    minecraft_image = convert_to_minecraft_style(image)

    # Display the result
    st.image(minecraft_image, caption="Minecraft 16x16 Style", use_column_width=True)

    # Download button for the image
    img_bytes = minecraft_image.tobytes
