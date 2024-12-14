import os
from PIL import Image  # For reading image files
import numpy as np


class ImageManager:
    """
    Manages image loading, conversion to NumPy arrays, and storing them in a dictionary.
    """

    def __init__(self):
        # Dictionary to store images as NumPy arrays
        self.image_dict = {}

    def add_image(self, project_name, image_path):
        """
        Loads an image from the specified path, converts it to a NumPy array, and saves it under a project name.
        :param project_name: Key for the dictionary, typically a project or image identifier.
        :param image_path: Path to the image file.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        img = Image.open(image_path).convert("RGB")  # Open and ensure RGB mode
        img_array = np.array(img)  # Convert to NumPy array

        # Save the image array under the project name
        if project_name not in self.image_dict:
            self.image_dict[project_name] = []
        self.image_dict[project_name].append(img_array)

    def get_images(self, project_name):
        """
        Retrieve all images (as NumPy arrays) associated with a project name.
        :param project_name: Key for the dictionary.
        :return: List of NumPy arrays or None if the key doesn't exist.
        """
        return self.image_dict.get(project_name, [])

    def list_projects(self):
        """
        List all project names in the dictionary.
        :return: List of project names.
        """
        return list(self.image_dict.keys())
