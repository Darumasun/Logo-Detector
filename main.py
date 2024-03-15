
from LogoDetector import LogoDetector

if __name__ == "__main__":
    service_account_key = "/Users/darumasun/W2023/Logo_Scaner/service_account.json"  # Replace with your service account
    logo_detector = LogoDetector(service_account_key)
    image_folder = "/Users/darumasun/W2023/Logo_Scaner/image_file"  # Replace with the path to your image file
    output_csv = "detected_logos.csv"  # Output CSV file name
    output_folder = "detected_images"  # Output folder name

    # The script includes the option to save images with detected logos (True/False)
    logo_detector.detect_logos(image_folder, output_csv, output_folder, True, 10)

