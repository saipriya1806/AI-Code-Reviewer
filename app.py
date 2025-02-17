import streamlit as st
import google.generativeai as genai
import os
from dotenv import find_dotenv, load_dotenv

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Load API Key from environment variable
api_key = os.getenv('GENAI_API_KEY')
if not api_key:
    st.error(" API key is missing. Please set the 'GENAI_API_KEY' environment variable.")
else:
    # Configure Google Gemini API
    genai.configure(api_key=api_key)

sys_prompt = """You are an advanced Python instructor and code reviewer.
Your task is to analyze the given Python code, identify potential bugs, logical errors, or areas for improvement, and provide suggestions. Focus solely on Python and coding questions, providing example-based explanations.

For any non-Python-related queries, refer the user to Google links, clarifying that you cannot answer those questions.

Please provide:
Identify and describe any bugs, errors, or areas of improvement in the code, including line numbers where applicable.
Provide a corrected version of the code.
Explain the changes made, detailing why they are necessary.
"""

gemini = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash-exp", 
    system_instruction=sys_prompt)

def app():
    st.set_page_config(
        page_title="AI Code Reviewer", 
        layout="centered"
        
    )

    st.title(" Python Code Reviewer")

    user_prompt = st.text_area("Enter your python code here...", height=200)

    if st.button("Generate"):
        if user_prompt.strip():
            with st.spinner("Analyzing your code..."):
                try:
                    response = gemini.generate_content(user_prompt)
                    st.header("Code Review")

                    # Improved display formatting
                    review_text = response.text
                    # Split the review into sections (Bug Report, Fixed Code, Explanation) 
                    sections = review_text.split("```") 

                    if len(sections) >= 3: 
                        bug_report = sections[0].strip()
                        fixed_code = sections[1].replace("python", "").strip() 
                        explanation = sections[2].strip()

                        st.subheader("Bug Report")
                        st.write(bug_report)

                        st.subheader("Fixed Code")
                        st.code(fixed_code, language="python")

                        st.subheader("Explanation")
                        st.write(explanation)
                    else:
                        st.write(review_text) 

                except Exception as e: # Catch potential errors during generation
                   st.error(f" An error occurred during code review: {e}")

        else:
            st.error(" Please enter your code before clicking 'Generate'.")

if __name__ == '__main__':
    app()
