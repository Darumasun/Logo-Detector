import csv
import os
from google.cloud import vision
from PIL import Image, ImageDraw
from tqdm import tqdm


class LogoDetector:
    # Initialize the LogoDetector class with service_account_key
    def __init__(self, service_account_key):
        # Check whether the service_account_key exits or not
        assert os.path.isfile(service_account_key), "Service account key file does not exist"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key
        # Create an instance of ImageAnnotatorClient which makes a request to the Google Cloud Vision API
        self.client = vision.ImageAnnotatorClient()

    # An integrated function
    def detect_logos(self, image_folder, output_csv, output_folder, save_detected_image, batch_size=10):
        # Check whether a file is a string ending with ".csv"
        assert isinstance(output_csv, str) and output_csv.endswith(".csv"), "A file must be a string ending with .csv."
        # Check whether a file is a string
        assert isinstance(output_folder, str), "A file must be a string"
        # Check whether a variable is boolean
        assert isinstance(save_detected_image, bool), "save_detected_image must be a boolean"
        # Check whether batch size is more than zero
        assert batch_size > 0, "Batch size must be greater than zero"

        # Create a list of file paths for all the files in the folder
        image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)]
        # Check whether image_paths is a list
        assert isinstance(image_paths, list), "Image paths should be a list"

        total_images = len(image_paths)
        detected_logos = []

        # Display the progress of iteration of batch processing
        # 0 to the total number of images with a step size of batch size
        for i in tqdm(range(0, total_images, batch_size), desc="Processing images", unit="batch"):
            # Extracts a batch of paths from the list of image paths
            batch_paths = image_paths[i:i + batch_size]
            # Use process_batch function to detect logos
            batch_logos = self.process_batch(batch_paths, output_folder, save_detected_image)
            # Add all elements from batch_logos to detected_logos
            detected_logos.extend(batch_logos)

        # Use write_to_csv function to write extracted elements into a csv file
        self.write_to_csv(detected_logos, output_csv)

    # A function to extract information using vision
    def process_batch(self, batch_paths, output_folder, save_detected_image):
        batch_logos = []

        for image_path in batch_paths:
            # It reads the contents of the image using binary mode
            with open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            # Using logo detection method
            response = self.client.logo_detection(image=image)
            # Retrieves the detected logo
            logos = response.logo_annotations

            if logos:
                for logo in logos:
                    # Construct logo data with description, score, original image path
                    logo_data = {'Description': logo.description, 'Score': logo.score, 'Original_Image': image_path}
                    # If save detected image is True, it generates a path and save logo images
                    if save_detected_image:
                        detected_image_path = os.path.join(output_folder,
                                                           f'detected_logo_{os.path.basename(image_path)}')
                        self.save_detected_image(image_path, detected_image_path, logo.bounding_poly)
                        logo_data['Detected_Image'] = detected_image_path
                    batch_logos.append(logo_data)
        return batch_logos

    # Save detected logo images into a new folder
    def save_detected_image(self, image_path, output_path, bounding_poly):
        # Creates the directory structure if it does not exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Opens an image
        im = Image.open(image_path)
        # Creates a drawing context
        draw = ImageDraw.Draw(im)
        # Extracts the coordinates of the vertices of the detected logo
        vertices = [(vertex.x, vertex.y) for vertex in bounding_poly.vertices]
        # Draws a polygon on an image
        draw.polygon(vertices, outline='red')
        # Extract a region of interest
        detected_logo_region = im.crop((vertices[0][0], vertices[0][1], vertices[2][0], vertices[2][1]))
        # Save an extracted region as an image
        detected_logo_region.save(output_path)

    # Write the information of the detected logos to a CSV file."
    def write_to_csv(self, detected_logos, output_csv):
        # Define field names
        fieldnames = ['Description', 'Score', 'Detected_Image', 'Original_Image']
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row
            writer.writeheader()
            for logo in detected_logos:
                writer.writerow(logo)
