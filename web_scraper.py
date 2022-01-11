import csv

from VAR import HEADERS


def individual_tournament_web_data_scraper(soup):
    """
    Scraps information from fis-website for individual tournament only.
    :param soup: BeautifulSoup object representing fis-web structure.
    :return: list with tuples representing line information about ranking/jumper name/nationality/total points.
    """
    # scrap tables for individual tournaments
    positions = soup.find_all('div', class_="g-lg-1 g-md-1 g-sm-1 g-xs-2 justify-right pr-1 gray bold")

    positions_list = []
    for position in positions:
        positions_list.append(position.text)

    names = soup.find_all('div', class_="g-lg g-md g-sm g-xs justify-left bold")

    name_list = []
    for name in names:
        name_list.append(name.text.strip())

    country_div = soup.find('div', id='events-info-results')
    country = country_div.find_all('span', class_='country__name-short')

    country_list = []
    for nationality in country:
        country_list.append(nationality.text)

    points = soup.find_all('div', class_='g-lg-2 g-md-2 g-sm-3 g-xs-5 justify-right blue bold')

    points_list = []
    for point in points:
        points_list.append(point.text.strip())

    # combine all list together
    rows = list(zip(positions_list, name_list, country_list, points_list))

    return rows


def team_tournament_web_data_scraper(soup):
    """
    Scraps information from fis-website for team tournament only.
    :param soup: BeautifulSoup object representing fis-web structure.
    :return: list with tuples representing line information about ranking/jumper name/nationality/total points.
    """
    # scrap tables for team tournaments
    ranking = soup.find_all('div', class_="g-lg-1 g-md-1 g-sm-1 g-xs-2 justify-right bold pr-1")

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
            rows.append(row)

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
