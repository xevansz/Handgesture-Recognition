# Import necessary libraries
import streamlit as st
import os
import subprocess
import aspose.slides as slides
import aspose.pydrawing as drawing

def convert_ppt_to_png(pptx_path, output_folder):
    # Load presentation
    pres = slides.Presentation(pptx_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Loop through slides
    for index in range(pres.slides.length):
        # Get reference to slide
        slide = pres.slides[index]

        # Save as image
        image_path = os.path.join(output_folder, f"{index + 1}.jpeg")
        slide.get_thumbnail().save(image_path, drawing.imaging.ImageFormat.jpeg)

    print("PPT is converted to image files.")

def main():
    # Set the title
    st.title("PRESENTATION CONTROL WITH HAND GESTURES:")
    st.title(" A Vision Based Approach")

    # File upload for presentation
    uploaded_file = st.file_uploader("Upload Presentation File (PPTX)", type=["pptx"])

    # Display convert slides button
    convert_slides_button = st.button("Convert Slides")

    # Display start button
    start_display_button = st.button("Start Display")

    # Handle start display button click
    if start_display_button:
        # Check if a presentation file is uploaded
        if uploaded_file is not None:
            # Set the target folder path
            target_folder = "Project"

            # Save the uploaded PPTX file
            pptx_path = os.path.join(target_folder, "presentation.pptx")
            with open(pptx_path, "wb") as pptx_file:
                pptx_file.write(uploaded_file.read())

            # Execute "gesture.py"
            process = subprocess.Popen(["python", "-u", "gesture.py"], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print("STDOUT:", stdout.decode('utf-8'))
            print("STDERR:", stderr.decode('utf-8'))
        else:
            print("Presentation file is not uploaded")

    # Handle convert slides button click
    if convert_slides_button:
        # Check if a presentation file is uploaded
        if uploaded_file is not None:
            # Set the target folder path for converted images
            output_folder = "PRESENTATION"

            # Save the uploaded PPTX file
            pptx_path = "pptxfile.pptx"
            with open(pptx_path, "wb") as pptx_file:
                pptx_file.write(uploaded_file.read())

            # Convert PPTX to PNG
            convert_ppt_to_png(pptx_path, output_folder)

            st.success("PPT is converted to PNGs.")

if __name__ == "__main__":
    main()
