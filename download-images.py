import csv
import os
import requests
from tqdm import tqdm

csv_file = "products_export.csv"
handle_header = "Handle"
image_src_header = "Image Src"

# Create a directory called Images if it doesn't exist already
if not os.path.exists("Images"):
    os.makedirs("Images")

# Read the CSV file
with open(csv_file, "r") as f:
    csv_reader = csv.DictReader(f)

    # Count total non-empty rows
    total_images = sum(1 for row in csv_reader if row[handle_header] and row[image_src_header])

    # Print the total number of images
    print(f"Total images to download: {total_images}")

    # Reset the CSV file reader to the beginning
    f.seek(0)
    csv_reader = csv.DictReader(f)

    # Initialize tqdm progress bar
    progress_bar = tqdm(total=total_images, desc="Downloading images")

    # Loop through each line of the CSV file
    for row in csv_reader:
        handle = row[handle_header]
        img_url = row[image_src_header]

        if not (handle and img_url):
            continue

        try:
            # Download the image
            response = requests.get(img_url)

            if response.status_code == 200:
                # Save the image to Images directory with the original image name without query parameters
                original_image_name = img_url.split("/")[-1].split("?")[0]
                filename = f"Images/{original_image_name}"
                with open(filename, "wb") as img_file:
                    img_file.write(response.content)

                # Update the progress bar
                progress_bar.update(1)
            else:
                print(f"[Error] Failed to download image for handle: {handle}. Status code: {response.status_code}")

        except Exception as e:
            print(f"[Error] Failed to download image for handle: {handle}. Error: {str(e)}")

    progress_bar.close()
    print("Successfully downloaded all images.")