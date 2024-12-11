import os
import csv
import re
import argparse
from datetime import datetime

def parse_filename(filepath):
    """
    Parse a filename in the format: 
    'date-vendor-subject-amountincents [invoicecode].pdf/jpg'
    
    Returns a dictionary with parsed components
    """
    # Remove the file extension
    filename = os.path.basename(filepath)
    # Remove the file extension
    filename_without_ext = os.path.splitext(filename)[0]
    
    # Split into main parts and invoice code
    try:
        # Split into main parts and optional invoice code
        parts = filename_without_ext.split(' ')

        if len(parts) > 1:
            # Filename with invoice code
            main_parts, invoice_code = ' '.join(parts[:-1]), parts[-1]
        else:
            # Filename without invoice code
            main_parts, invoice_code = parts[0], ''
        
        # Split the main parts
        date, vendor, subject, amount = main_parts.split('-')

        # Convert date from YYYY-MM-DD to DD/MM/YYYY
        formatted_date = datetime.strptime(date, '%Y%m%d').strftime('%d/%m/%Y')
        
        return {
            'Date': formatted_date,
            '_SortDate': datetime.strptime(date, '%Y%m%d'),  # Hidden key for sorting
            'Vendor': vendor,
            'Subject': subject,
            'Amount': int(amount) / 100,  # Convert cents to dollars
            'Invoice Code': invoice_code
        }
        
    except ValueError:
        # If parsing fails, return None or handle as needed
        print(f"Could not parse filename: {filename}")
        return None

def convert_filenames_to_csv(folder_path, output_csv_path):
    """
    Convert all filenames in a folder to a CSV file
    """
    # Validate input folder
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return
    
    # Get all PDF and JPG files in the folder
    supported_extensions = ['.pdf', '.jpg', '.jpeg']
    files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in supported_extensions]
    
    if not files:
        print(f"No supported files found in the folder: {folder_path}")
        return
    
    # Parse filenames
    parsed_data = [parse_filename(os.path.join(folder_path, file)) for file in files]

    # Remove any None values (failed parses)
    parsed_data = [entry for entry in parsed_data if entry is not None]

    parsed_data_sorted = sorted(parsed_data, key=lambda x: x['_SortDate'])
    
    # Write to CSV
    if parsed_data_sorted:
        keys = ['Date', 'Vendor', 'Subject', 'Amount', 'Invoice Code']
        with open(output_csv_path, 'w', newline='') as csvfile:
            dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
            dict_writer.writeheader()
            
            # Write sorted data, creating new dicts without the sorting key
            for entry in parsed_data_sorted:
                csv_entry = {k: entry[k] for k in keys}
                dict_writer.writerow(csv_entry)
        
        print(f"CSV file created at {output_csv_path}")
    else:
        print("No valid files found to parse.")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Convert PDF filenames to a structured CSV.')
    parser.add_argument('input_folder', help='Path to the folder containing PDF files')
    parser.add_argument('-o', '--output', 
                        default=None, 
                        help='Path for the output CSV file (optional)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no output path specified, create one in the input folder
    if args.output is None:
        output_csv_path = os.path.join(args.input_folder, 'invoicedata.csv')
    else:
        output_csv_path = args.output
    
    # Convert filenames to CSV
    convert_filenames_to_csv(args.input_folder, output_csv_path)

if __name__ == '__main__':
    main()
