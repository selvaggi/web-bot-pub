from PyPDF2 import PdfReader, PdfWriter
import os

def reduce_pdf_size(pdf_path, output_path, size_limit_mb=10):
    # Check the initial size of the PDF
    
    ## convert in bytes
    size_limit=size_limit_mb*1024*1024
    initial_size = os.path.getsize(pdf_path)
    if initial_size <= size_limit:
        print("PDF is already under the size limit.")
        return pdf_path
    
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    for remove_pages in range(1, total_pages):
        writer = PdfWriter()
        
        # Add pages except the last 'remove_pages' number of pages
        for page_num in range(total_pages - remove_pages):
            writer.add_page(reader.pages[page_num])
        
        # Save to a temporary file to check size
        temp_output_path = output_path.rsplit('.', 1)[0] + '_temp.pdf'
        with open(temp_output_path, 'wb') as f_out:
            writer.write(f_out)
        
        # Check if the file size is within the limit now
        if os.path.getsize(temp_output_path) <= size_limit:
            os.rename(temp_output_path, output_path)
            print(f"Reduced PDF size to under {size_limit} bytes by removing {remove_pages} pages.")
            return output_path
        else:
            os.remove(temp_output_path)  # Clean up temp file
    
    print("Unable to reduce the PDF size under the limit by removing pages.")
    return None

# Example usage
pdf_path = './filename.pdf'  # Replace with your PDF file path
output_path = './reduced_file.pdf'  # Replace with your desired output file path
min_size_mb = 5
reduce_pdf_size(pdf_path, output_path, min_size_mb)
