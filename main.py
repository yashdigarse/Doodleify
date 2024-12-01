import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import requests
from io import BytesIO

# Load the Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

st.title('Image-to-Image Conversion with Hugging Face and Streamlit')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    # Convert the image using the model
    prompt = "a photo of an astronaut riding a horse on mars"  # Example prompt
    result = pipe(prompt, init_image=image, strength=0.75, guidance_scale=7.5)
    
    # Display the output image
    output_image = result.images[0]
    st.image(output_image, caption='Output Image.', use_column_width=True)