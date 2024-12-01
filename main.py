import streamlit as st
from PIL import Image
import torch
from torchvision import transforms
from diffusers import StableDiffusionImg2ImgPipeline

# Load your model
@st.cache_resource
def load_model():
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

# Title and Instructions
st.title("Image-to-Image Model Demo")
st.write("Upload an image and apply transformations using a model.")

# Upload Image
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Parameters
    st.subheader("Modify Parameters")
    strength = st.slider("Transformation Strength", 0.1, 1.0, 0.5)

    # Transform the Image
    if st.button("Transform Image"):
        st.write("Applying transformation...")

        pipe = load_model()
        output = pipe(prompt="a fantasy painting of the uploaded image",
                      image=image,
                      strength=strength).images[0]

        st.image(output, caption="Transformed Image", use_column_width=True)
