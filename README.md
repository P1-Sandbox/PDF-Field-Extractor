# pdf-field-extractor
A Python script to extract and parse field data from PDF files into CSV format.

## Background

This script was created based on a project that required exporting and importing field data from one application to another. It simplifies the process of extracting field information from PDF files, making it easier to transfer and integrate data between different systems.

## Features

- Extracts text content from PDF files.
- Parses field labels, types, and IDs from structured tables in the PDF.
- Saves the extracted data into a CSV file for easy access and analysis.
- Automatically handles permission issues when writing to files, saving to a user-accessible location if needed.

## Requirements

- Python 3.x
- `PyPDF2` library

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/pdf-to-csv-parser.git
   cd pdf-to-csv-parser
