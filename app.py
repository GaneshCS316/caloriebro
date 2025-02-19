import streamlit as st
import google.generativeai as genai 
import os 
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(image_data, mime_type):
    image_parts = [
        {
            "mime_type": mime_type,
            "data": image_data
        }
    ]
    return image_parts

# Frontend of the app
st.set_page_config(page_title="Calories Advisor App")
st.header("Calorie Bro")

# Camera input
uploaded_file = st.camera_input("Take a photo")

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Captured Image.')

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert nutritionist. You need to see the food items from the image and calculate the total calories, also provide the details of every food item with calorie intake in the below format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----

Finally, mention whether the food is healthy or not and also mention the percentage split of the ratio of carbohydrates, fats, proteins, fibers, sugar, and other things required in our diet.
"""

if submit and uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    mime_type = uploaded_file.type
    image_data = input_image_setup(bytes_data, mime_type)
    response = get_gemini_response(input_prompt, image_data)
    st.header("The response is")
    st.write(response)
