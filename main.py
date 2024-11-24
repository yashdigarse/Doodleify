import streamlit as st
import requests
from PIL import Image
import io

def cartoonify_image(image_file):
    url = "https://cartoon-image.p.rapidapi.com/cartoon"
    
    headers = {
        "X-RapidAPI-Key": "58c8cb483emshb1f84eba4a5f694p1ab7cbjsn87bda417be10",
        "X-RapidAPI-Host": "cartoon-image.p.rapidapi.com"
    }
    
    files = {"image": image_file.getvalue()}
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

st.title("Image Cartoonifier")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Original Image", use_column_width=True)
    
    if st.button("Cartoonify"):
        with st.spinner("Cartoonifying..."):
            cartoon_image = cartoonify_image(uploaded_file)
        
        if cartoon_image:
            st.image(cartoon_image, caption="Cartoonified Image", use_column_width=True)
            
            # Provide download button
            buf = io.BytesIO()
            cartoon_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="Download Cartoonified Image",
                data=byte_im,
                file_name="cartoonified_image.png",
                mime="image/png"
            )