# logo-detector
LogoDetector is a Python-based tool designed to automate the process of recognizing and cataloging logos from images within a specified folder. Utilizing the powerful Google Cloud Vision API, this script scans each image for logos, extracts relevant information, and saves the results into a CSV file for easy review and analysis. It supports batch processing for scalability, allowing efficient handling of large datasets ranging from a few images to tens of thousands.
# Features
- Google Cloud Vision API Integration: Harnesses the logo detection capabilities of Google Cloud Vision for accurate and fast logo recognition.
- Batch Processing: Includes functionality to process images in batches, configurable through a parameter, optimizing performance for large datasets.
- Progress Visualization: Utilizes the tqdm package to provide real-time progress feedback during the logo detection process.
- Sanity Checks: Implements assert statements for input validation, ensuring reliability and correctness of the input parameters.
- Optional Image Saving: Offers the option to save images with detected logos marked, facilitating visual verification of the detection results.
- CSV Output: Compiles and saves detected logo information (description, score, and image paths) into a structured CSV file for further use or analysis.
# Usage
1. Ensure you have a Google Cloud Vision API key and the google-cloud-vision, PIL, and tqdm packages installed.
2. Instantiate the LogoDetector class with your Google Cloud service account key.
3. Call the detect_logos method with the appropriate parameters, including the input folder path, output CSV file name, output folder for detected images (optional), and batch size.
