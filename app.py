# Import necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

# Configure genai with api key
genai.configure(api_key=st.secrets["api_key"])

# Setup the model
generation_config = {
    "temperature": 0.4, # the lower the temperature the less creative the model will become
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# apply safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompt = """

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thorughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendation and Next Steps: Based on your analysis, suggest potential next steps, including further testsor treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to determined based on the provided image.'
3. Disclaimer: Accompany your analysis with disclaimer: "Consult with a Doctor before making any decisions."
4. Your insights are valuable in guiding clinical decision. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide me an output response with 4 headings: Detailed Analysis, Findings Report, Recommendation and Next Steps, Treatment Suggestions
"""

# Model Configuration
model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Set the page configuration

st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

# Set the logo
st.image("medical_logo.jpg", width=150)

# Set the title
st.title("👩🏻‍⚕Vital❤Image📷 Analytics📊👨🏻‍⚕")

# Set the subtitle
st.subheader("An application that can help users to identify Medical Images")

uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, width=500, caption="Uploaded Medical Image")
submit_button = st.button("Generate the Analysis") 

if submit_button:
    # processes the uploaded image
    image_data = uploaded_file.getvalue()
    
    # making our image ready
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]
    
    # Getting our prompt ready
    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]
    
    # Generate a response based on prompt and image
    
    response = model.generate_content(prompt_parts)
    
    if response:
        st.title("Here is the analysis based on your image: ")
        st.write(response.text) 
