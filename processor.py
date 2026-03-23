import os
from PIL import Image, ImageFilter

class ImageProcessor:
    def __init__(self, input_path, output_folder="processed_outputs"):
        self.input_path = input_path
        self.output_folder = output_folder
        # Extract the filename without the extension (e.g., 'photo' from 'photo.jpg')
        self.filename = os.path.splitext(os.path.basename(input_path))
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def generate_all(self):
        """Runs all transformations and returns a list of created file paths."""
        results = [
            self.generate_thumbnail(),
            self.generate_grayscale(),
            self.generate_blur()
        ]
        return results

    def generate_thumbnail(self, size=(128, 128)):
        with Image.open(self.input_path) as img:
            img.thumbnail(size)
            path = os.path.join(self.output_folder, f"{self.filename}_thumb.jpg")
            # Convert to RGB to ensure it can be saved as JPEG (handles PNG transparency)
            img.convert("RGB").save(path, "JPEG")
            return path

    def generate_grayscale(self):
        with Image.open(self.input_path) as img:
            grayscale_img = img.convert("L")
            path = os.path.join(self.output_folder, f"{self.filename}_gray.jpg")
            grayscale_img.save(path, "JPEG")
            return path

    def generate_blur(self, radius=5):
        with Image.open(self.input_path) as img:
            blurred_img = img.filter(ImageFilter.GaussianBlur(radius))
            path = os.path.join(self.output_folder, f"{self.filename}_blurred.jpg")
            blurred_img.convert("RGB").save(path, "JPEG")
            return path

# --- Local Testing Block ---
if __name__ == "__main__":
    # Test this by putting any image in the folder and naming it 'test.jpg'
    TEST_IMAGE = "test.jpg" 
    
    if os.path.exists(TEST_IMAGE):
        processor = ImageProcessor(TEST_IMAGE)
        print(f"Processing {TEST_IMAGE}...")
        created_files = processor.generate_all()
        print(f"Success! Created: {created_files}")
    else:
        print(f"Please add an image named '{TEST_IMAGE}' to the folder to test.")