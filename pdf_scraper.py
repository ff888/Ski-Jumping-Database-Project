import pdfplumber
import csv

from pdf_data_converter import text_pdfs_scraper_individual, table_pdfs_scraper_individual, team_pdf_scraper
from helpers import clear_tables, clear_text, clear_team_text, clear_team_tables
from VAR import HEADERS


def raw_data_from_pdfs(fis_pdf):
    """
    Function extracts tabular data from pdf in two ways (1. extracting tables, 2. extracting text from tables
    if pdfplumber can't read tables.
    :param fis_pdf: pdf file in the same directory
    :return: lists of rows with jumper data
    """

    fis_pdf = fis_pdf + '.pdf'

    # unpacking pdf
    pdf_file = pdfplumber.open(fis_pdf)

    pages = pdf_file.pages

    # helpers lists to handle data
    content_for_list = []
    content_for_text = []
    extracted_data = []

    for page in pages:

        # unpack pdfs with tables
        if len(page.extract_tables()) > 0:
            print('pdf with tables')
            content_for_list.append(page.extract_tables())

        else:
            # unpack pdfs with text
            print('pdf with text')
            text = page.extract_text()

            content_for_text.append(text.split('\n')[9:])

    # data from tables-pdfs
    cleared_data_tables = clear_tables(content_for_list)
    csv_data_table = table_pdfs_scraper_individual(cleared_data_tables)

    for row in csv_data_table:
        extracted_data.append(row)

    # data from text-pdfs
    cleared_data_text = clear_text(content_for_text)
    csv_data_text = text_pdfs_scraper_individual(cleared_data_text)

    for row in csv_data_text:
        extracted_data.append(row)

    return extracted_data


def raw_data_for_team_pdfs(fis_pdf):
    """

    :param data:
    :return:
    """

    fis_pdf = fis_pdf + '.pdf'

    # unpacking pdf
    pdf_file = pdfplumber.open(fis_pdf)

    pages = pdf_file.pages

    text_team_list = []

    # extract pdfs
    for page in pages:
        print('text team pdf')

        text_team_list.append(page.extract_text())

    clear_data_from_text = clear_team_text(text_team_list)


def create_csv_file_from_pdf_data(pdf_name, extracted_data):
    """
    Function creates csv file with data extracted from pdf, also creates same name as pdf name.
    """

    file_name = pdf_name + '.csv'

    with open(file_name, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADERS)
        writer.writerows(extracted_data)
