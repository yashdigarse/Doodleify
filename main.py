import streamlit as st
from PIL import Image
import requests
import io
# Define the function to apply the cartoon effect
def apply_cartoon_effect(image_data, api_key):
    url = 'https://api.lightxeditor.com/external/api/v1/cartoon'
    headers = {
        'x-api-key': api_key,  # Replace with your actual API key
        'Content-Type': 'application/json'
    }
    files = {'image': image_data}
    data = {
        "styleImageUrl": "https://ai.flux-image.com/flux/d4533a74-9d35-4683-8a05-18c0b646ad36.jpg",  # Replace with the URL of your input style image
        "textPrompt": "Cartoon style with vibrant colors and exaggerated features"  # Replace with your specific input prompt
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    return response

# Streamlit app layout
st.title("Cartoon Effect App")

# Input fields
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

api_key = "e456a84c544e4576bd71888f4e8f7d98_fd59cad6cf8848e98b2b28abf80b12f4_andoraitools"

# Button to trigger the cartoon effect
if st.button("Apply Cartoon Effect"):
    if uploaded_file is not None:
        image_data = uploaded_file.read()
        response = apply_cartoon_effect(image_data, api_key)
        
        # Check if the request was successful
        if response.status_code == 200:
            st.success("Request was successful!")
            response_json = response.json()
            output_url = response_json.get("body", {}).get("output")
            if output_url:
                st.image(output_url, caption="Cartoon Effect Image")
            else:
                st.error("Output URL not found in the response.")
        else:
            st.error(f"Request failed with status code: {response.status_code}")
            st.text(response.text)
    else:
        st.error("Please upload an image.")