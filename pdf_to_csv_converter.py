import csv
import re
import os
import tempfile
import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def parse_pdf_content(content):
    # Split the content into lines
    lines = content.split('\n')
    
    # Find the start of the fields table
    start_index = -1
    for i, line in enumerate(lines):
        if 'Field Label' in line and 'Type' in line and 'Field Id' in line:
            start_index = i
            break
    
    if start_index == -1:
        print("Could not find the start of the fields table. Here's a sample of the PDF content:")
        print('\n'.join(lines[:20]))  # Print first 20 lines for debugging
        return []
    
    # Extract the relevant lines
    field_lines = lines[start_index + 1:]  # Start from the line after the header
    
    # Parse the fields
    fields = []
    current_field = {}
    for line in field_lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if this line starts a new field
        parts = line.split()
        if len(parts) >= 3 and parts[-1].isdigit():
            if current_field:
                fields.append(current_field)
            current_field = {
                'Field Label': ' '.join(parts[:-2]),
                'Type': parts[-2],
                'Field Id': parts[-1]
            }
        elif current_field and 'Relationship' not in current_field:
            # This must be the relationship
            current_field['Relationship'] = line
    
    # Add the last field
    if current_field:
        fields.append(current_field)
    
    return fields

def write_csv(fields, filename='students_fields.csv'):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Field Label', 'Type', 'Relationship', 'Field Id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for field in fields:
                writer.writerow(field)
        return filename
    except PermissionError:
        # If we don't have permission to write in the current directory,
        # try to write in the user's home directory
        home_dir = os.path.expanduser("~")
        new_filename = os.path.join(home_dir, filename)
        try:
            with open(new_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Field Label', 'Type', 'Relationship', 'Field Id']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for field in fields:
                    writer.writerow(field)
            return new_filename
        except PermissionError:
            # If we still don't have permission, use a temporary file
            temp_dir = tempfile.gettempdir()
            temp_filename = os.path.join(temp_dir, filename)
            with open(temp_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Field Label', 'Type', 'Relationship', 'Field Id']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for field in fields:
                    writer.writerow(field)
            return temp_filename

def pdf_to_csv(pdf_path, csv_filename='students_fields.csv'):
    try:
        # Extract text from PDF
        pdf_content = extract_text_from_pdf(pdf_path)
        
        # Parse the content
        fields = parse_pdf_content(pdf_content)
        
        if not fields:
            print("No fields were extracted. Please check the PDF content.")
            return
        
        # Write to CSV
        output_filename = write_csv(fields, csv_filename)
        
        print(f"CSV file '{output_filename}' has been created with {len(fields)} fields.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Sample usage place file path here
pdf_to_csv('C:/Users/ncayo3/OneDrive - Georgia Institute of Technology/Documents/SAM Demo - Fields.pdf')

print("Press Enter to exit...")
input()