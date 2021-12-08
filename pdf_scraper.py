import pdfplumber
from pdf_data_converter import pdf_with_no_tables_scraper, table_scraper_individual
from helpers import clear_tables


def raw_data_from_tables(fis_pdf, cod):
    """
    Function extracts tabular data from pdf.
    :param fis_pdf: pdf file in the same directory
    :return: lists of rows with jumper data
    """

    all_content = []

    fis_pdf = fis_pdf + '.pdf'

    # unpacking pdf
    pdf_file = pdfplumber.open(fis_pdf)

    page_1 = pdf_file.pages[0]
    content_page_1 = page_1.extract_tables()

    # for pdf that pdfplumber not see tables
    if len(content_page_1) == 0:
        print('PDF with no tables!')

        page_2 = pdf_file.pages[1]

        content_1 = page_1.extract_text().split('\n')[16:-2]
        content_2 = page_2.extract_text().split('\n')[7:-2]

        content = content_1 + content_2

        # clear rows
        raw_content = []
        data_to_skip = ['Club', 'Rank', 'Name', 'Fini', 'not ', 'Disq', 'Did ', 'Code', 'PRAG', 'NOC ', 'Not ']

        for row in content:
            line = row.split('\n')

            if line[0][0:4] in data_to_skip:
                continue
            elif line[0] == 'Weather Information':
                break

            raw_content.append(line)

        all_content = pdf_with_no_tables_scraper(raw_content, cod)

    # pdf with only 1 page
    elif len(pdf_file.pages) == 1:
        print('PDF with 1 page')
        pass

    # pdf with 2 pages
    elif len(pdf_file.pages) == 2:
        print('PDF with 2 pages')
        pass

    # pdf with 3 pages
    elif len(pdf_file.pages) == 3 and len(page_1.extract_tables()) > 0:
        print('PDF with 3 pages')
        pass

    else:
        print('PDF with more then 3 pages')
        pass

    return all_content, cod


def create_csv_file(pdf_name, extracted_data):
    """
    Function creates csv file with data extracted from pdf, also creates same name as pdf name.
    """

    file_name = pdf_name + '.csv'

    with open(file_name, 'w') as fh:
        fh.writelines(extracted_data)
