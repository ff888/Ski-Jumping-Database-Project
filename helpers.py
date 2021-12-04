import datetime as dt
import requests


def file_name_creator(soup):
    """
    Function checks fis web and creates a file name using scraped information from there.
    Name structure: Year-Month-Day_City_TournamentType_HillSize_Gender_Team/Individual (2018-Mar-25_Oberstdorf(GER)_WC_NH_W_I)
    :param soup: web parser by BeautifulSoup (soup)
    :return: file name as a string
    """

    # city name where the tournament held
    city = soup.h1.text.replace(' ', '').replace('/', '')

    # gender and type of tournament check
    info_line = soup.find('div', class_='event-header__kind').text

    if "Men's Team" in info_line:
        gender = 'M'
        team_or_ind = 'T'
    elif "Women's Team" in info_line:
        gender = 'W'
        team_or_ind = 'T'
    elif "Mixed Team" in info_line:
        gender = 'X'
        team_or_ind = 'T'
    elif "Women's" in info_line:
        gender = 'W'
        team_or_ind = 'I'
    elif "Men's" in info_line:
        gender = 'M'
        team_or_ind = 'I'
    else:
        gender = '?'
        team_or_ind = '?'
        print('Team/ind or gender info not valid: ', info_line)

    # hill size
    if 'Normal Hill' in info_line or 'Normal H.' in info_line or 'NH' in info_line:
        hill = 'NH'
    elif 'Large Hill' in info_line:
        hill = 'LH'
    elif 'Flying Hill' in info_line:
        hill = 'SF'
    else:
        if info_line.split()[-1][0] == 'K':
            if int(info_line.split()[-1].strip('K')) <= 44:
                hill = 'SH'
            elif int(info_line.split()[-1].strip('K')) <= 74:
                hill = 'MH'
            elif int(info_line.split()[-1].strip('K')) <= 99:
                hill = 'NH'
            elif int(info_line.split()[-1].strip('K')) <= 169:
                hill = 'LH'
            elif int(info_line.split()[-1].strip('K')) >= 170:
                hill = 'SF'

        elif info_line.split()[-1][0:2] == 'HS':
            if int(info_line.split()[-1].strip('HS')) <= 49:
                hill = 'SH'
            elif int(info_line.split()[-1].strip('HS')) <= 84:
                hill = 'MH'
            elif int(info_line.split()[-1].strip('HS')) <= 109:
                hill = 'NH'
            elif int(info_line.split()[-1].strip('HS')) <= 184:
                hill = 'LH'
            elif int(info_line.split()[-1].strip('HS')) >= 185:
                hill = 'SF'
        else:
            hill = '??'
            print('Hill size not defined: ', info_line)

    # type of the tournament
    tournament_type = soup.find('div', class_='event-header__subtitle').text

    if tournament_type == 'World Cup':
        short_tournament_type = 'WC'
    elif tournament_type == 'World Ski Championships':
        short_tournament_type = 'CH'
    elif tournament_type == 'Olympic Winter Games':
        short_tournament_type = 'OL'
    elif tournament_type == 'FIS Ski-Flying World Championships':
        short_tournament_type = 'SF'
    elif tournament_type == 'Qualification':
        short_tournament_type = 'QA'
    elif tournament_type == 'Grand Prix':
        short_tournament_type = 'GP'
    else:
        short_tournament_type = '??'
        print('Tournament name not valid: ', tournament_type)

    # date
    date_to_format = soup.find('span', class_='date__short').text.split()

    year = date_to_format[2]
    month = date_to_format[0]
    day = date_to_format[1].strip(',')

    date_to_format = year + '-' + month + '-' + day
    date = dt.datetime.strptime(date_to_format, '%Y-%b-%d').date()

    new_file_name = f'{date}_{city}_{short_tournament_type}_{hill}_{gender}_{team_or_ind}'

    return new_file_name


def download_pdf(soup, file_name):
    """
    Checks if PDF (with tournament results) is exists on given website, if yes downloads it.
    :param soup: BeautifulSoup object representing fis-web structure.
    :param file_name: string with date/city/type/hill/gender/
    :return: it is downloads file not returns anything.
    """

    divs = soup.find_all('div', class_='table-row pointer js-false-link')

    pdf_name = file_name + '.pdf'

    link_list = []
    file_name_text_list = []

    file_name_html = soup.find_all('div', class_='g-lg-10 g-md-11 g-sm-10 g-xs-10 justify-left')

    for div in divs:
        link_list.append(div.get('data-link'))

    for file_name in file_name_html:
        file_name_text_list.append(file_name.text)

    if 'Official Results' in file_name_text_list:
        for link in link_list:
            if link[-6:] == 'RL.pdf':
                pdf_link = requests.get(link)

                with open(pdf_name, "wb") as f:
                    f.write(pdf_link.content)

            elif link[-7:] == 'RL4.pdf':
                pdf_link = requests.get(link)

                with open(pdf_name, "wb") as f:
                    f.write(pdf_link.content)

    elif 'Result 2nd Round' in file_name_text_list:
        for link in link_list:
            if link[-7:] == 'RL2.pdf':
                pdf_link = requests.get(link)

                with open(pdf_name, "wb") as f:
                    f.write(pdf_link.content)

    elif 'Results 1st Round' in file_name_text_list:
        for link in link_list:
            if link[-7:] == 'RL1.pdf':
                pdf_link = requests.get(link)

                with open(pdf_name, "wb") as f:
                    f.write(pdf_link.content)


def team_points_creator():
    """
    Creates team points value by adding total points by 4 first jumpers from each nationality. If the team consists of 3
     jumpers, her/his points are added twice. If the team consists of two or one people total_points = 'NULL'
    :return: team_points
    """
    pass


def team_ranking_creator():
    """
    Creates team ranking based on team_points value.
    :return: team_points
    """
    pass


def clear_tables(data):
    """
    Function clears table if rows are not valid (dasen't hold jumper data).
    :param data: raw data from the pdf tables
    :return: cleared raw data
    """
    rows_to_skip = [x.lower() for x in ['Jury', 'RACE', 'RANK', 'CLUB', 'not ', 'TIME', 'WIND', '1st ', 'Fina', 'GATE',
                                        'No. ', 'TECH', 'CHIE', 'ASSI', 'EQUI', 'Name', 'Comp', 'Stat', 'Disq', 'Not ',
                                        'Did ', 'Weat', 'NOTE', 'Lege', 'Worl', 'NOC ', '2nd ']]

    all_content = []

    for all_table_lists in data:
        for row in all_table_lists:
            if row[0] is None:
                continue
            elif row[0][0:4].lower() in rows_to_skip:
                continue
            elif len(row) > 1 and row[1] in ('Time', 'Gate'):
                continue
            else:
                all_content.append(row)

    return all_content


def disqualification_no_tables_file_check(row):
    """
    Function checks if there was a disqualification of jumper and created a csv dsq row.
    :param row: jumper row information.
    :return:
    """

    name = '?'
    nationality = '?'

    for element in row:
        for el in element:

            # skip elements (line)
            if el[0].split()[0] == 'Reason' or el[0].split()[0] == 'SCE':
                continue

            # skip if second last elements is SCE
            if el.split()[-2] == 'SCE':

                name = ' '.join(el.split()[1:-3]).title()
                nationality = el.split()[-3]

            else:
                name = ' '.join(el.split()[1:-1]).title()
                nationality = el.split()[-1]

    ranking = 'DSQ'
    dob = 'NULL'
    club = 'NULL'
    speed_1 = 'NULL'
    distance_1 = 'NULL'
    judge_marks_1a = 'NULL'
    judge_marks_1b = 'NULL'
    judge_marks_1c = 'NULL'
    judge_marks_1d = 'NULL'
    judge_marks_1e = 'NULL'
    judge_marks_points_jump_1 = 'NULL'
    round_1_total_points = 'NULL'
    round_1_ranking = 'DSQ'
    speed_2 = 'NULL'
    distance_2 = 'NULL'
    judge_marks_2a = 'NULL'
    judge_marks_2b = 'NULL'
    judge_marks_2c = 'NULL'
    judge_marks_2d = 'NULL'
    judge_marks_2e = 'NULL'
    judge_marks_points_jump_2 = 'NULL'
    round_2_total_points = 'NULL'
    round_2_ranking = 'NULL'
    total_points = 'NULL'

    jumper_line = [ranking, name, dob, nationality, club, speed_1, distance_1, judge_marks_1a, judge_marks_1b,
                   judge_marks_1b, judge_marks_1c, judge_marks_1d, judge_marks_1e, judge_marks_points_jump_1,
                   round_1_total_points, round_1_ranking, speed_2, distance_2, judge_marks_2a, judge_marks_2b,
                   judge_marks_2c, judge_marks_2d, judge_marks_2e, judge_marks_points_jump_2, round_2_total_points,
                   round_2_ranking, total_points]

    return jumper_line


def disqualification_check(row):
    """
    Function checks if there was a disqualification of jumper and created a csv dsq row.
    :param row: jumper row information.
    :return: jumper disqualification row
    """

    # find disqualification jumper row
    name = '?'
    nationality = '?'

    if len(row) == 1:
        if 'green' in row[0].split():
            name = ' '.join(row[0].split()[2:-6]).title()
            nationality = row[0].split()[-6]
        else:
            name = ' '.join(row[0].split()[2:-1]).title()
            nationality = row[0].split()[-1]

    elif len(row) == 2:
        if len(row[1].split()) >= 3:
            name = ' '.join(row[1].split()[:-1]).title()
            nationality = row[1].split()[-1]

        elif len(row[0].split()) >= 4:
            name = ' '.join(row[0].split()[1:-1]).title()
            nationality = row[0].split()[-1]

    elif len(row) == 3:
        name = ' '.join(row[1].split()[:-1]).title()
        nationality = row[1].split()[-1]

    ranking = 'DSQ'
    dob = 'NULL'
    club = 'NULL'
    speed_1 = 'NULL'
    speed_2 = 'NULL'
    distance_1 = 'NULL'
    distance_2 = 'NULL'
    judge_marks_1a = 'NULL'
    judge_marks_1b = 'NULL'
    judge_marks_1c = 'NULL'
    judge_marks_1d = 'NULL'
    judge_marks_1e = 'NULL'
    judge_marks_2a = 'NULL'
    judge_marks_2b = 'NULL'
    judge_marks_2c = 'NULL'
    judge_marks_2d = 'NULL'
    judge_marks_2e = 'NULL'
    round_1_total_points = 'NULL'
    round_2_total_points = 'NULL'
    round_ranking_1 = 'DSQ'
    round_ranking_2 = 'NULL'
    total_points = 'NULL'

    jumper_row = [ranking, name, dob, nationality, club, speed_1, speed_2, distance_1, distance_2,
                  judge_marks_1a, judge_marks_1b, judge_marks_1c, judge_marks_1d, judge_marks_1e,
                  judge_marks_2a, judge_marks_2b, judge_marks_2c, judge_marks_2d, judge_marks_2e,
                  round_1_total_points, round_2_total_points, round_ranking_1, round_ranking_2, total_points]

    return jumper_row
