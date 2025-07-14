# Import necessary libraries
import streamlit as st
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

def convert_pptx_to_pdf(pptx_path, pdf_path):
    """Convert PowerPoint presentation to PDF using LibreOffice."""
    try:
        # Use LibreOffice to convert PPTX to PDF
        cmd = [
            'libreoffice', 
            '--headless', 
            '--convert-to', 'pdf', 
            '--outdir', 'data/slides/pdf',
            pptx_path
        ]
        
        st.info("🔄 Converting PPTX to PDF using LibreOffice...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # LibreOffice saves with the same name but .pdf extension in the output dir
            pdf_basename = os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf"
            expected_pdf = os.path.join("data/slides/pdf", pdf_basename)
            if os.path.exists(expected_pdf):
                # Move to our desired location
                shutil.move(expected_pdf, pdf_path)
                st.success("✅ PPTX converted to PDF successfully!")
                return True
            else:
                st.error(f"❌ PDF file not found at expected location: {expected_pdf}")
                return False
        else:
            st.error(f"❌ LibreOffice conversion failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        st.error("❌ LibreOffice conversion timed out")
        return False
    except Exception as e:
        st.error(f"❌ Error converting PPTX to PDF: {e}")
        return False

def convert_pdf_to_images(pdf_path, output_folder):
    """Convert PDF to PNG images using pdf2image."""
    try:
        from pdf2image import convert_from_path
        
        st.info("🔄 Converting PDF to images...")
        
        # Check if PDF exists
        if not os.path.exists(pdf_path):
            st.error(f"PDF file '{pdf_path}' not found!")
            return False
        
        # Create output directory if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Convert PDF to images
        images = convert_from_path(
            pdf_path,
            dpi=200,
            use_cropbox=False,
            use_pdftocairo=True
        )
        
        # Save each page as an image
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"{i + 1}.png")
            image.save(image_path, "PNG")
        
        # Count the generated images
        image_files = [f for f in os.listdir(output_folder) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        st.success(f"✅ Converted PDF to {len(image_files)} images")
        return True
        
    except Exception as e:
        st.error(f"❌ Error converting PDF to images: {e}")
        return False

def convert_ppt_to_png(pptx_path, output_folder):
    """Convert PowerPoint presentation to PNG images using new workflow."""
    try:
        # Create temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Step 1: Convert PPTX to PDF
            pdf_path = os.path.join(temp_dir, "presentation.pdf")
            if not convert_pptx_to_pdf(pptx_path, pdf_path):
                return False
            
            # Step 2: Convert PDF to PNG images
            if not convert_pdf_to_images(pdf_path, output_folder):
                return False
            
            return True
            
    except Exception as e:
        st.error(f"❌ Error in conversion workflow: {e}")
        return False

def cleanup_presentation_files(pptx_path=None, pdf_path=None):
    """Clean up presentation files after completion."""
    try:
        # Clean up images directory
        images_dir = "data/slides/images"
        if os.path.exists(images_dir):
            for file in os.listdir(images_dir):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    os.remove(os.path.join(images_dir, file))
            st.success("🧹 Cleaned up presentation images")
        
        # Ask user about PPTX file cleanup
        if pptx_path and os.path.exists(pptx_path):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Keep PPTX file", type="secondary"):
                    # Only remove PDF file, keep PPTX
                    if pdf_path and os.path.exists(pdf_path):
                        os.remove(pdf_path)
                    st.success("💾 Kept PPTX file, removed PDF")
                    return True
            
            with col2:
                if st.button("🗑️ Remove PPTX file too", type="secondary"):
                    # Remove both PPTX and PDF files
                    os.remove(pptx_path)
                    if pdf_path and os.path.exists(pdf_path):
                        os.remove(pdf_path)
                    st.success("🗑️ Removed PPTX and PDF files")
                    return True
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error during cleanup: {e}")
        return False

def main():
    """Main Streamlit application."""
    
    # Set page config
    st.set_page_config(
        page_title="HandGesture Recognition",
        page_icon="🎤",
        layout="wide"
    )
    
    # Header
    st.title("🎤 HandGesture Recognition")
    st.subheader("Control Presentations with Hand Gestures")
    st.markdown("---")

    # Navigation - vertical display
    st.sidebar.title("Navigation")
    
    if st.sidebar.button("📤 Upload & Convert", use_container_width=True):
        st.session_state.page = "Upload & Convert"
    
    if st.sidebar.button("🎮 Gesture Control", use_container_width=True):
        st.session_state.page = "Gesture Control"
    
    if st.sidebar.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "Settings"
    
    # Default page
    if 'page' not in st.session_state:
        st.session_state.page = "Upload & Convert"
    
    if st.session_state.page == "Upload & Convert":
        upload_and_convert_page()
    elif st.session_state.page == "Gesture Control":
        gesture_control_page()
    elif st.session_state.page == "Settings":
        settings_page()

def upload_and_convert_page():
    """Page for uploading and converting presentations."""
    st.header("📤 Upload & Convert Presentation")
    # Define paths at the top for DRYness
    pptx_path = "data/pptx/uploaded_presentation.pptx"
    pdf_path = "data/slides/pdf/uploaded_presentation.pdf"
    images_dir = "data/slides/images"
    # File upload for presentation
    uploaded_file = st.file_uploader(
        "Upload Presentation File (PPTX)", 
        type=["pptx"],
        help="Select a PowerPoint presentation file"
    )
    col1, col2 = st.columns(2)
    with col1:
        # Convert slides button
        if st.button("🔄 Convert Slides", type="primary"):
            if uploaded_file is not None:
                os.makedirs("data/pptx", exist_ok=True)
                os.makedirs("data/slides/pdf", exist_ok=True)
                with open(pptx_path, "wb") as pptx_file:
                    pptx_file.write(uploaded_file.read())
                # Convert PPTX to images
                output_folder = images_dir
                if convert_ppt_to_png(pptx_path, output_folder):
                    st.success("✅ Slides converted successfully!")
                    st.info("💡 You can now use gesture control to navigate through the slides.")
            else:
                st.warning("⚠️ Please upload a presentation file first.")
    with col2:
        start, stop = st.columns(2)
        # Track process state in session_state
        if 'gesture_process' not in st.session_state:
            st.session_state.gesture_process = None
        # Status indicator
        if st.session_state.gesture_process is not None and st.session_state.gesture_process.poll() is None:
            st.success("Gesture controller is running.")
            process_running = True
        else:
            process_running = False
            st.session_state.gesture_process = None
        with start:
            if st.button("🎮 Start Gesture Control", disabled=process_running):
                if os.path.exists(images_dir) and len(os.listdir(images_dir)) > 0:
                    st.info("🚀 Starting gesture controller...")
                    try:
                        process = subprocess.Popen(
                            ["python", "src/gesture.py"], 
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            start_new_session=True
                        )
                        st.session_state.gesture_process = process
                        st.success("✅ Gesture controller started in background!")
                    except Exception as e:
                        st.error(f"❌ Failed to start gesture controller: {e}")
                else:
                    st.warning("⚠️ Please convert slides first before starting gesture control.")
        with stop:
            if st.button("🛑 Stop Presenting", type="secondary", disabled=not process_running):
                st.info("Attempting to stop gesture controller and clean up camera...")
                try:
                    if st.session_state.gesture_process is not None:
                        st.session_state.gesture_process.terminate()
                        st.session_state.gesture_process = None
                    if sys.platform.startswith('linux') or sys.platform == 'darwin':
                        subprocess.run("pkill -f 'python.*gesture.py'", shell=True)
                        subprocess.run("fuser -k /dev/video0", shell=True)
                    elif sys.platform == 'win32':
                        subprocess.run("taskkill /F /IM python.exe /T", shell=True)
                    st.success("🛑 Presentation stopped. Camera and windows cleaned up.")
                except Exception as e:
                    st.error(f"Error stopping presentation: {e}")
    # Cleanup section
    st.markdown("---")
    st.subheader("🧹 Cleanup After Presentation")
    if os.path.exists(images_dir) and len(os.listdir(images_dir)) > 0:
        st.info("💡 After your presentation is complete, you can clean up the files:")
        if st.button("🧹 Clean Up Files", type="primary"):
            cleanup_presentation_files(pptx_path, pdf_path)
    else:
        st.info("💡 No presentation files to clean up yet.")
    # Display current slides
    if os.path.exists(images_dir):
        slides_count = len([f for f in os.listdir(images_dir) 
                          if f.lower().endswith((".png", ".jpg", ".jpeg"))])
        if slides_count > 0:
            st.subheader(f"📊 Current Slides ({slides_count} total)")
            # Show first few slides as preview
            slide_files = sorted([f for f in os.listdir(images_dir) 
                                if f.lower().endswith((".png", ".jpg", ".jpeg"))])
            cols = st.columns(min(3, len(slide_files)))
            for i, slide_file in enumerate(slide_files[:3]):
                with cols[i]:
                    slide_path = os.path.join(images_dir, slide_file)
                    st.image(slide_path, caption=f"Slide {i+1}", use_container_width=True)

def gesture_control_page():
    """Page for gesture control information."""
    st.header("🎮 Gesture Control Guide")
    
    st.markdown(""" 
    ### Hand Gestures
    
    Position your hand at face level (above the green threshold line) and use these gestures:
    
    | Gesture | Action | Finger Pattern |
    |---------|--------|----------------|
    | 👆 Index finger only | Previous slide / Draw | `[1, 0, 0, 0, 0]` |
    | 👍 Thumb up | Next slide | `[0, 0, 0, 0, 1]` |
    | 👆 Index finger | Draw/Annotate | `[0, 1, 0, 0, 0]` |
    | 🤟 Three fingers | Erase annotation | `[0, 1, 1, 1, 0]` |
    | ✌️ Two fingers | Pointer mode | `[0, 1, 1, 0, 0]` |
    
    ### Keyboard Shortcuts
    
    - `q`: Quit the application
    - `r`: Reset all annotations
    - `n`: Next slide
    - `p`: Previous slide
    
    ### Tips for Best Results
    
    1. **Lighting**: Ensure good, consistent lighting
    2. **Background**: Use plain backgrounds
    3. **Distance**: Keep hand 1-2 feet from camera
    4. **Stability**: Minimize camera movement
    5. **Position**: Keep hand above the green threshold line
    """)

def settings_page():
    """Page for configuration settings."""
    st.header("⚙️ Settings")
    
    st.subheader("Configuration")
    
    if os.path.exists("config/gesture_config.json"):
        with open("config/gesture_config.json", "r") as f:
            import json
            config = json.load(f)
        
        st.json(config)
        
        if st.button("📝 Edit Configuration"):
            st.info("💡 Edit the config/gesture_config.json file to customize settings.")
    else:
        st.warning("⚠️ Configuration file not found.")

if __name__ == "__main__":
    main() 