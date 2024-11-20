import streamlit as st
from PIL import Image
import requests
import io
# Define the function to apply the cartoon effect
def apply_cartoon_effect(image_data, api_key):
    url = 'https://api.rapidapi.com/cartoon-generator'
    headers = {
        'x-rapidapi-key': api_key,  # Replace with your actual API key
        'x-rapidapi-host': 'api.rapidapi.com',
        'Content-Type': 'application/octet-stream'
    }
    response = requests.post(url, headers=headers, data=image_data)
    return response

# Streamlit app layout
st.title("AI Cartoon Generator")

# Input fields
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
api_key = "58c8cb483emshb1f84eba4a5f694p1ab7cbjsn87bda417be10"

# Button to trigger the cartoon effect
if st.button("Generate Cartoon"):
    if uploaded_file is not None:
        image_data = uploaded_file.read()
        response = apply_cartoon_effect(image_data, api_key)
        
        # Check if the request was successful
        if response.status_code == 200:
            st.success("Request was successful!")
            response_json = response.json()
            output_url = response_json.get("output")
            if output_url:
                st.image(output_url, caption="Cartoon Effect Image")
            else:
                st.error("Output URL not found in the response.")
        else:
            st.error(f"Request failed with status code: {response.status_code}")
            st.text(response.text)
    else:
        st.error("Please upload an image.")