import textwrap
from helpers import disqualification_check


def pdf_with_no_tables_scraper(row_data):
    """
    Pdfs database contains exceptions where pdfplumber cannot find the table. The function takes row data and organizes
    data into rows of information formatted in csv.
    :param row_data: unformatted data from pdf
    :return: formatted data into csv
    """
    print('pdf wit no tables scraper')
    
    # data list length counter
    n = int(len(row_data) / 3)

    # jumper raw data list of lists creator
    jumper_content = []

    for _ in range(n):
        jumper_row_list = [row_data[0], row_data[1], row_data[2]]
        jumper_content.append(jumper_row_list)
        del row_data[0:3]


    pass


def table_scraper_individual(raw_data):
    """
    Function takes row data from pdfs tables and converts it to csv.
    :param raw_data: data from pdf tables extracted by pdfplumber
    :return: formatted data into csv
    """
    print('pdf table scraper with tables')

    pass
