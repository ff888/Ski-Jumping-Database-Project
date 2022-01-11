import pdfplumber
import csv

from pdf_data_converter import pdf_with_no_tables_scraper, table_scraper_individual
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
    table_raw_content_list = []

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

    # clean rows for pdfs with tables
    data_to_skip = ['Jury', 'RACE', 'Club', 'Rank', 'Name', 'Fini', 'not ', 'Disq', 'Code', 'PRAG', 'NOC ',
                    'Not ', 'TIME', 'WIND', 'Fina', 'GATE', 'No. D', 'Comp', 'Worl', 'FIS ']

    data_to_skip = list(x.lower() for x in data_to_skip)

    for lines in content_for_list:
        for line in lines:
            for row in line:

                if row[0] is None:
                    continue
                if row[0][0:4].lower() in data_to_skip:
                    continue
                if row[0] in ['Weather Information', 'Statistics', '1st Round', 'Did Not Start', 'Qualification']:
                    break
                if row[0][0:18] == 'Technical Delegate':
                    break
                if row[0][0:4] == 'NOTE':
                    break

                # DSQ row have to handle
                if row[0] == '' or row[0].split()[0] in ['DNS', 'DSQ']:
                    continue
                if 'SCE 4' in row or 'ICR' in row[2] or 'SCE' in row[2]:
                    continue

                table_raw_content_list.append(row)

    tables_extracted_to_csv_list = table_scraper_individual(table_raw_content_list)

    return tables_extracted_to_csv_list


def create_csv_file_from_pdf_data(pdf_name, extracted_data):
    """
    Function creates csv file with data extracted from pdf, also creates same name as pdf name.
    """

    file_name = pdf_name + '.csv'

    with open(file_name, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADERS)
        writer.writerows(extracted_data)
