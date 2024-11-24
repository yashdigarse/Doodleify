import streamlit as st
from PIL import Image
import numpy as np

def create_minecraft_character(image, block_size=16):
    # Resize the image to Minecraft-like character size
    small_image = image.resize((block_size, block_size), Image.NEAREST)
    
    # Upscale back to original size for better visibility
    minecraft_character = small_image.resize((block_size * 16, block_size * 16), Image.NEAREST)
    return minecraft_character

def apply_minecraft_palette(image):
    # Define a simple Minecraft-inspired color palette
    palette = [
        (20, 20, 20),    # Black
        (255, 255, 255), # White
        (128, 128, 128), # Gray
        (0, 255, 0),     # Green
        (255, 0, 0),     # Red
        (0, 0, 255),     # Blue
        (255, 255, 0),   # Yellow
        (165, 42, 42)    # Brown
    ]
    
    # Convert image to numpy array
    image_np = np.array(image)
    
    # Flatten the array and map each pixel to the closest color in the palette
    reshaped = image_np.reshape((-1, 3))
    distances = np.linalg.norm(reshaped[:, None] - np.array(palette), axis=2)
    nearest_color_indices = distances.argmin(axis=1)
    mapped_pixels = np.array(palette)[nearest_color_indices]
    
    # Reshape back to the original image size
    new_image = mapped_pixels.reshape(image_np.shape)
    return Image.fromarray(np.uint8(new_image))

st.title("Convert Your Photo to a Minecraft Character!")
st.write("Upload a photo, and turn it into a Minecraft-style character.")

# Upload the image
uploaded_image = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_image:
    original_image = Image.open(uploaded_image).convert("RGB")
    st.image(original_image, caption="Original Image", use_column_width=True)

    # Options for block size and palette
    st.write("### Settings")
    block_size = st.slider("Minecraft Block Size (Character Resolution)", 8, 32, 16)
    use_palette = st.checkbox("Apply Minecraft-like Color Palette")

    # Process the image
    resized_image = create_minecraft_character(original_image, block_size)
    if use_palette:
        resized_image = apply_minecraft_palette(resized_image)
    
    # Display the result
    st.image(resized_image, caption="Minecraft Character", use_column_width=True)

    # Download option
    resized_image.save("minecraft_character.png")
    with open("minecraft_character.png", "rb") as file:
        st.download_button(
            label="Download Minecraft Character",
            data=file,
            file_name="minecraft_character.png",
            mime="image/png",
        )
