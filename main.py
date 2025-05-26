import streamlit as st
import PyPDF2
import io
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

st.set_page_config(page_title="AI Resume Critik", page_icon="📄", layout="centered" )

st.title("AI Resume Critik")
st.markdown("Upload your resume and get a detailed AI powered analysis of your resume.")

uploaded_file = st.file_uploader("Upload your resume (PDF Format)", type=["pdf"])

job_role = st.text_input("Enter the job role you are applying for (optional)")

analyze = st.button("Analyze Resume")



def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("No text found in the uploaded file.")
            st.stop()
        prompt = f"""
        You are a resume analysis expert. Analyze the following resume and provide constructive feedback on the resume. Focus on the following areas:
        1. Content clarity and impact
        2. Formatting and readability
        3. Skills Presentation
        4. Experience descriptions
        5. Specific improvements for {job_role if job_role else "General Job Applications" }

        Resume content:
        {file_content}

        Provide your feedback in a clear and concise manner, focusing on specific improvements and actionable steps and then below that give an updated resume with the improvements (mention that it is a draft).
        """
        
        # Create a model instance
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate the response
        response = model.generate_content(prompt)
        
        st.markdown("## Resume Analysis Feedback")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()