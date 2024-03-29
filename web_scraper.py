import csv

from helpers import find_index
from VAR import HEADERS, nation_list


def individual_tournament_web_data_scraper(soup):
    """
    Scraps information from fis-website for individual tournament only.
    :param soup: BeautifulSoup object representing fis-web structure.
    :return: list with tuples representing line information about ranking/jumper name/nationality/total points.
    """
    # scrap tables for individual tournaments
    table = soup.find('div', id='events-info-results')
    rows = table.find_all('div', class_="g-row justify-sb")

    table_row_list = []
    for row in rows:

        jumper_row = row.text.split()
        # get ranking
        ranking = jumper_row[0]

        # get nationality -> use it's index
        nationality_index = find_index(jumper_row, nation_list)
        nationality = jumper_row[nationality_index].upper()

        # fix error
        if nationality == 'FR':
            nationality = 'FRA'
        if nationality == 'BRD':
            nationality = 'GER'

        # get name - une nationality index
        if jumper_row[nationality_index - 1].isnumeric():
            name = ' '.join(jumper_row[2:nationality_index - 1]).title()
        else:
            name = ' '.join(jumper_row[2:nationality_index]).title()

        # get total points
        if jumper_row[-1] in nation_list:
            total_points = 'NULL'
        else:
            total_points = jumper_row[-2]

        jumper_data_row = [
            ranking, name, nationality, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
            'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
            'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', total_points, 'NULL', 'NULL']

        table_row_list.append(jumper_data_row)

    return table_row_list


def team_tournament_web_data_scraper(soup):
    """
    Scraps information from fis-website for team tournament only.
    :param soup: BeautifulSoup object representing fis-web structure.
    :return: list with tuples representing line information about ranking/jumper name/nationality/total points.
    """
    # scrap tables for team tournaments
    # scrap tables for individual tournaments
    table = soup.find('div', id='events-info-results')

    for row in table:
        jumper_row = row.text.split()
        if len(jumper_row) == 0:
            continue

        # remove extra item
        jumper_row = [item for item in jumper_row if item not in ['THE', 'REPUBLIC']]

        # create list with nationality indexes
        national_index_list = []
        for national in jumper_row:
            if national in nation_list:
                national_index_list.append(jumper_row.index(national))
        national_index_list = [(item-3) for item in national_index_list]

        teams_list = []
        for num in range(len(national_index_list)+1):
            teams_list.append(jumper_row[national_index_list[0]:national_index_list[1]])
            del national_index_list[0]
            if len(national_index_list) == 1:
                teams_list.append(jumper_row[national_index_list[0]:])
                break

        jumper_data_row = []
        for team in teams_list:
            if len(team) in [0, 1]:
                continue

            rank = team[0]
            nat = team[3]
            team_points = team[4]

            name_list_with_no_numeric_val = []
            for item in team[6:]:
                if item.isalpha() and item != 'x' or '-' in item:
                    name_list_with_no_numeric_val.append(item + '+')

                else:
                    name_list_with_no_numeric_val.append('*****')

            jumper_list = ''.join(name_list_with_no_numeric_val).split('*****')
            jumper_list = [i for i in jumper_list if i != '']
            for jumper in jumper_list:
                jumper = jumper.rstrip('+').rstrip('+*****')
                jumper = jumper.replace('+', ' ').title()

                # in some cases web using xxxx instead of date-year skip this err
                if 'Xxxx' in jumper:
                    continue

                jumper_data_row.append([
                    rank, jumper, nat, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
                    'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
                    'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
                    team_points, rank])

        return jumper_data_row


def save_web_team_into_csv(data, file_name):
    """
    Save info from web team tournaments (only before 2002) into csv file, plus add HEADERS to the file
    :param data: tournament table information scrape from web
    :param file_name: name of the file info taken from web
    """
    with open(file_name + '.csv', 'a') as fh:
        csv_writer = csv.writer(fh)
        csv_writer.writerow(HEADERS)
        for row in data:
            csv_writer.writerow(row)


def save_into_csv_file_web(data, file_name):
    """
    Creates csv file using date scraped from fis-webs and saves into csv file.
    :param data: list of tuples (individual_tournament_data_scraper)
    :param file_name: file name (file_name_creator)
    """

    with open(file_name + '.csv', 'a') as fh:
        csv_writer = csv.writer(fh)

        csv_writer.writerow(HEADERS)

        dob = 'NULL'
        club = 'NULL'
        distance_jump_1 = 'NULL'
        distance_points_1 = 'NULL'
        speed_jump_1 = 'NULL'
        judge_marks_jump_1a = 'NULL'
        judge_marks_jump_1b = 'NULL'
        judge_marks_jump_1c = 'NULL'
        judge_marks_jump_1d = 'NULL'
        judge_marks_jump_1e = 'NULL'
        judge_total_points_1 = 'NULL'
        gate_jump_1 = 'NULL'
        gate_compensation_1 = 'NULL'
        wind_jump_1 = 'NULL'
        wind_compensation_1 = 'NULL'
        total_points_jump_1 = 'NULL'
        ranking_jump_1 = 'NULL'
        distance_jump_2 = 'NULL'
        distance_points_2 = 'NULL'
        speed_jump_2 = 'NULL'
        judge_marks_jump_2a = 'NULL'
        judge_marks_jump_2b = 'NULL'
        judge_marks_jump_2c = 'NULL'
        judge_marks_jump_2d = 'NULL'
        judge_marks_jump_2e = 'NULL'
        judge_total_points_2 = 'NULL'
        gate_jump_2 = 'NULL'
        gate_compensation_2 = 'NULL'
        wind_jump_2 = 'NULL'
        wind_compensation_2 = 'NULL'
        total_points_jump_2 = 'NULL'
        ranking_jump_2 = 'NULL'
        team_points = 'NULL'
        team_ranking = 'NULL'

        for line in data:

            ranking = line[0]
            name = line[1]
            nationality = line[2]
            total_points = line[3]

            row = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1, speed_jump_1,
                   judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c, judge_marks_jump_1d,
                   judge_marks_jump_1e, judge_total_points_1, gate_jump_1, gate_compensation_1, wind_jump_1,
                   wind_compensation_1, total_points_jump_1, ranking_jump_1, distance_jump_2, distance_points_2,
                   speed_jump_2, judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                   judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2, wind_jump_2,
                   wind_compensation_2, total_points_jump_2, ranking_jump_2, total_points, team_points, team_ranking]

            csv_writer.writerow(row)
