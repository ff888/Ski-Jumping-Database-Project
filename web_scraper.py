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
    rows = table.find_all('div', class_="g-row justify-sb")

    table_row_list = []
    for row in table:
        jumper_row = row.text.split()
        if len(jumper_row) == 0:
            continue

        # remove extra item
        jumper_row = [item for item in jumper_row if item != 'REPUBLIC']

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

        jumper_row_filtered = []
        for team in teams_list:
            rank = team[0]
            nat = team[3]
            team_points = team[4]

            # skip all numerical data to pull only names
            jumpers_names = [item for item in team[6:] if item.isalpha()]



            """jumpers_names = [item for item in team[6:] if item.isalpha()]
            
            for name in jumpers_names:
                names_joined_list = []
                if name[1:].islower():
                    names_joined_list.append(name)"""








    """ranking = soup.find_all('div', class_="g-lg-1 g-md-1 g-sm-1 g-xs-2 justify-right bold pr-1")

    ranking_list = []
    for r in ranking:
        ranking_list.append(r.text)

    total_points = soup.find_all('div', class_="g-lg-2 g-md-2 g-sm-3 g-xs-5 justify-right")

    total_points_list = []
    for p in total_points:
        if p.text != '':
            total_points_list.append(p.text)

    jumper = soup.find_all('div', class_="g-lg-17 g-md-17 g-sm-13 g-xs-11 justify-left bold")

    jumper_list = []
    for j in jumper:
        jumper_list.append(j.text.strip())

    nationalities_list = []
    for n in jumper_list[0::5]:
        if n == 'JAPAN':
            nation = 'JPN'
        elif n == 'SWITZERLAND':
            nation = 'SUI'
        else:
            nation = n[0:3]

        nationalities_list.append(nation)

    jumper_1 = jumper_list[1::5]
    jumper_2 = jumper_list[2::5]
    jumper_3 = jumper_list[3::5]
    jumper_4 = jumper_list[4::5]

    jumpers_team = list(zip(jumper_1, jumper_2, jumper_3, jumper_4))
    rank_points = list(zip(ranking_list, nationalities_list, total_points_list))
    lines = list(zip(jumpers_team, rank_points))

    rows = []
    for line in lines:
        rank = line[1][0]
        nat = line[1][1]
        pt = line[1][2]

        for jump in line[0]:
            row = (rank, jump, nat, pt)
            rows.append(row)"""

    return rows


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
