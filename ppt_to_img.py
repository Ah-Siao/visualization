import subprocess
import os

def ppt_to_images(ppt_file):
    # Create a temporary directory to store images
    temp_dir = "ppt_images"
    os.makedirs(temp_dir, exist_ok=True)

    # Command to convert PPT to images using LibreOffice (headless mode)
    cmd = [
        "libreoffice", "--headless", "--convert-to", "png",
        "--outdir", temp_dir, ppt_file
    ]
    
    subprocess.run(cmd, check=True)
    
    # Get the list of image paths
    images = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith(".png")]
    return images



def display_ppt(self, ppt_path):
    self.selected_project = "PPT"
    # Convert PPT slides to images
    ppt_images = ppt_to_images(ppt_path)

    # Display the PPT slides as images in the layout
    for image_path in ppt_images:
        pixmap = QPixmap(image_path)

        label = QLabel()
        label.setPixmap(pixmap)
        self.content_layout.addWidget(label)
