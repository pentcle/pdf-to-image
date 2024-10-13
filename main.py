import os
from pdf2image import convert_from_path
from PIL import Image
import shutil


# Clear the output directory before processing
def clear_output_directory(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)


# Save image as high-quality JPEG
def save_as_jpeg(image, output_path, quality=70):
    # Save the image as a JPEG with specified quality
    image.save(output_path, 'JPEG', quality=quality, optimize=True)


# Convert PDF to high-quality JPEG
def pdf_to_jpeg(pdf_file, output_folder, dpi=72, width=1200, quality=75):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_file, dpi=dpi)

    # Save each page as a high-quality JPEG with sequential numbering and prefixed filename
    for i, page in enumerate(pages):
        # Resize the image to the specified width (while keeping the aspect ratio)
        page = page.resize((width, int((float(page.size[1]) / page.size[0]) * width)))

        # Prefix the file name with sequential numbering
        base_filename = os.path.basename(pdf_file).replace('.pdf', '')

        # Convert to lowercase, replace spaces and underscores with hyphens
        base_filename_cleaned = base_filename.lower().replace(' ', '-').replace('_', '-')

        numbered_filename = f"{i + 1:02d}-{base_filename_cleaned}.jpg"  # e.g., 01-filename.jpg

        # Define the output file path
        jpeg_output = os.path.join(output_folder, numbered_filename)

        # Save the image as a high-quality JPEG
        save_as_jpeg(page, jpeg_output, quality)

    print(f"Conversion complete for {pdf_file}. JPEG files are saved in {output_folder}")


# Process all PDF files in the 'input' directory
def process_all_pdfs(input_folder, output_folder):
    # Clear the output folder before processing
    clear_output_directory(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_file = os.path.join(input_folder, filename)
            pdf_to_jpeg(pdf_file, output_folder)


# Example usage
input_folder = 'input'
output_folder = 'output'
process_all_pdfs(input_folder, output_folder)
