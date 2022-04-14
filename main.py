import requests

from bs4 import BeautifulSoup
from VAR import *
from pdf_scraper import raw_data_from_pdfs, raw_data_for_team_pdfs, create_csv_file_from_pdf_data
from helpers import file_name_creator, download_pdf
from web_scraper import \
    individual_tournament_web_data_scraper,\
    save_into_csv_file_web, \
    team_tournament_web_data_scraper
from db_create_and_save import creating_db


def main():
    for cod in range(2325, 3000):
        print()
        print(cod)

        if cod in [2019, 2021, 5059, 3528, 3499, 6350, 6351, 6353, 6354]:
            continue

        page = requests.get(f'https://www.fis-ski.com/DB/general/results.html?sectorcode=JP&raceid={cod}#down') # cookies=cookies, allow_redirects=False

        # path to the app
        PATH = "/Users/pik/PycharmProjects/pythonProject/Ski_Jumping_Data_Base_Project"

        # check page status
        if page.status_code == 404:
            print('code 404')
            pass

        elif page.status_code == 200:
            soup = BeautifulSoup(page.content, 'lxml')

            # check if competition cancelled
            if soup.find('div', class_='event-status event-status_cancelled'):
                print('Competition cancelled')
                continue

            # check for invalid competition city name and skip it
            if soup.h1.text in ('Four Hills Tournament (FIS)', 'Raw Air Tournament (FIS)', 'Russia Blue Bird (FIS)',
                                'Russia Blue Bird Tournament (FIS)'):
                continue
            if soup.h1.text is None:
                continue

            try:
                empty_web = soup.find('div', class_='g-xs-24 g-md center gray bold')

                if empty_web.text == 'No results found for this competition.':
                    print(empty_web.text)
                    continue

            except AttributeError:
                pass

            file_name = file_name_creator(soup, cod)
            print(file_name)

            # check only for World Cap/Grand Prix/Olympic/World Championship skip the rest.
            short_tournament_type = ['WC', 'GP', 'OL', 'CH']

            if file_name[-9:-7] in short_tournament_type:

                # pdf file for each event after 2002 that holds detailed information about tournament
                if int(file_name[0:4]) >= 2002:

                    # pdf for individual tournaments 2002 and after
                    if file_name[-1] == 'I':
                        print('Individual PDF')

                        # download pdf
                        download_pdf(soup, file_name)

                        # unpack tabular data
                        data = raw_data_from_pdfs(file_name)

                        # save data into csv file
                        create_csv_file_from_pdf_data(file_name, data)

                        # save into DB
                        creating_db(PATH)

                    # for team and mixed competition 2002 and after (pdfs)
                    elif file_name[-1] == 'T' or file_name[-1] == 'X':
                        print('Team PDF')

                        # download pdf
                        download_pdf(soup, file_name)

                        # unpack tabular data
                        data = raw_data_for_team_pdfs(file_name)

                        # save data into csv file
                        create_csv_file_from_pdf_data(file_name, data)

                        # save into DB
                        creating_db(PATH)

                # before 2002 data is on websites only
                elif int(file_name[0:4]) < 2002:

                    # for individual (web)
                    if file_name[-1] == 'I':
                        print('Individual WEB')

                        # save csv file
                        data = individual_tournament_web_data_scraper(soup)
                        save_into_csv_file_web(data, file_name)
                        creating_db(PATH)

                    # for Team or Mixed (web)
                    elif file_name[-1] == 'T':
                        print('Team WEB')

                        # save csv file
                        data = team_tournament_web_data_scraper(soup)
                        save_into_csv_file_web(data, file_name)
                        creating_db(PATH)


if __name__ == '__main__':
    main()
