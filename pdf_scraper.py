import pdfplumber
import csv

from pdf_data_converter import pdf_with_no_tables_scraper, table_scraper_individual
from helpers import clear_tables
from VAR import HEADERS


def raw_data_from_tables(fis_pdf):
    """
    Function extracts tabular data from pdf in two ways (1. extracting tables, 2. extracting text from tables
    if pdfplumber can't read tables.
    :param fis_pdf: pdf file in the same directory
    :return: lists of rows with jumper data
    """
    # helpers lists to handle data
    content_for_list = []
    content_for_text = []
    extracted_data = []

    fis_pdf = fis_pdf + '.pdf'

    # unpacking pdf
    pdf_file = pdfplumber.open(fis_pdf)

    pages = pdf_file.pages

    for page in pages:

        # unpack pdfs with tables
        if len(page.extract_tables()) > 0:
            print('pdf with tables')
            content_for_list.append(page.extract_tables())

        else:

            # unpack pdfs with text
            print('pdf with text')
            content_for_text.append(page.extract_text())

    # data from tables
    cleared_data_tables = clear_tables(content_for_list)
    csv_data = table_scraper_individual(cleared_data_tables)

    for row in csv_data:
        extracted_data.append(row)

    return extracted_data


def create_csv_file_from_pdf_data(pdf_name, extracted_data):
    """
    Function creates csv file with data extracted from pdf, also creates same name as pdf name.
    """

    file_name = pdf_name + '.csv'

    with open(file_name, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADERS)
        writer.writerows(extracted_data)
