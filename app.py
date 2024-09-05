import streamlit as st
import os
import time
from PyPDF2 import PdfReader

# Function to parse PDF text
def parse_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Main Streamlit UI
def main():
    st.title("PDF Text Extractor")

    # Initialize session state variables if they don't exist
    if 'uploaded_file_path' not in st.session_state:
        st.session_state.uploaded_file_path = None

    # Radio button to choose between default PDF or uploading a PDF
    option = st.radio(
        "Select an option:",
        ('Use Default PDF', 'Upload Your Own PDF')
    )

    # If "Use Default PDF" is selected
    if option == 'Use Default PDF':
        default_pdf_path = "pdf_NOC.pdf"  # Specify the default PDF path here
        if os.path.exists(default_pdf_path):
            st.write(f"Default PDF selected: {default_pdf_path}")
            if st.button("Get Text"):
                parsed_text = parse_pdf(default_pdf_path)
                st.text_area("Parsed Text", parsed_text, height=300)
        else:
            st.error(f"Default PDF not found at {default_pdf_path}")

    # If "Upload Your Own PDF" is selected
    elif option == 'Upload Your Own PDF':
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        
        if uploaded_file is not None:
            # Only create folder and save file if it hasn't been uploaded yet in this session
            if st.session_state.uploaded_file_path is None:
                # Generate a folder name using timestamp
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                folder_name = f"uploaded_{timestamp}_input_folder"
                os.makedirs(folder_name, exist_ok=True)
                
                # Save the uploaded PDF in the created directory
                file_path = os.path.join(folder_name, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Store the file path in session state
                st.session_state.uploaded_file_path = file_path
                st.success(f"File successfully uploaded and saved to {file_path}")
        
        # If the file has already been uploaded, display the button to parse and get the text
        if st.session_state.uploaded_file_path:
            if st.button("Get Text"):
                parsed_text = parse_pdf(st.session_state.uploaded_file_path)
                st.text_area("Parsed Text", parsed_text, height=300)

if __name__ == "__main__":
    main()
