import streamlit as st
from src.logic import spectra_reader


def show():
    st.title("File upload")

    # Make 2 columns
    col1, col2 = st.columns(2)

    # Column 1
    with col1:
        # radio buttons that indicate the type of file to upload
        file_type = st.radio("File type", ["Spectrum", "Target"])

    # Column 2
    with col2:
        # Upload file button, if pressed, show file uploader
        file = st.file_uploader("Upload file", type=["txt"]) # TODO: add more file types + multiple files
        if file is not None:
            # Get file name
            file_name = file.name
            file_string = file.read().decode("utf-8")

            # Show upload button to confirm upload
            if st.button("Confirm upload"):
                # If file type is spectra, read the spectra
                if file_type == "Spectrum":
                    spectra_reader.save_spectra_txt(file_name, file_string)

                # If file type is target, read the target
                elif file_type == "Target":
                    print("TODO: upload target")

                # Clear the file uploader
                st.empty()
