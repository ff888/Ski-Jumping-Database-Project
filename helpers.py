import datetime as dt
import requests
import itertools



def file_name_creator(soup, cod):
    """
    Function checks fis web and creates a file name using scraped information from there.
    Name structure: Year-Month-Day_City_TournamentType_HillSize_Gender_Team/Individual (2018-Mar-25_Oberstdorf(GER)_WC_NH_W_I)
    :param soup: web parser by BeautifulSoup (soup)
    :return: file name as a string
    """

    # city name where the tournament held
    city = soup.h1.text.replace(' ', '').replace('/', '')

    if ',' in city:
        city = city.split(',')[0] + city.split(',')[1][2:]

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
    elif 'Flying Hill' in info_line or "Men's Team Flying H." in info_line:
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

    new_file_name = f'{date}_{city}_({cod})_{short_tournament_type}_{hill}_{gender}_{team_or_ind}'

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

    table_raw_content_list = []

    # clean rows for pdfs with tables
    data_to_skip = ['Jury', 'RACE', 'Club', 'Rank', 'Name', 'Fini', 'not ', 'Disq', 'Code', 'PRAG', 'NOC ',
                    'Not ', 'TIME', 'WIND', 'Fina', 'GATE', 'No. D', 'Comp', 'Worl', 'FIS ']

    data_to_skip = list(x.lower() for x in data_to_skip)

    for lines in data:
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

    return table_raw_content_list


def clear_text(data):
    """


    :param data:
    :return:
    """

    raw_content_list = []

    # clean rows for pdfs with tables
    data_to_skip = ['Jury', 'RACE', 'Club', 'Rank', 'Name', 'Fini', 'not ', 'Disq', 'Code', 'PRAG', 'NOC ', 'Did ',
                    'Not ', 'TIME', 'WIND', 'Fina', 'GATE', 'No. D', 'Comp', 'Worl', 'FIS ', 'Chie', 'Tech', 'Assi',
                    'Equi', '1st ', 'www.']

    data_to_skip = list(x.lower() for x in data_to_skip)

    # skip not valid rows
    for rows in data:
        for row in rows:
            if row[0:4].lower() in data_to_skip:
                continue
            if row[0] == '(' and row[-1] == ')' or row == 'SC BACHMAYER Johann (AUT)':
                continue
            if row.split()[0] in ['Weather', 'FIS', 'Air', 'Report:', 'www.fis-', 'Statistics', 'Reason', 'Temp.[°C]',
                                  'ICR', 'Base']:
                break
            if row.split()[1] == 'Report':
                continue
            if row.split()[0][0:3] == 'SJM':
                continue

            raw_content_list.append(row)

    # create jumper list
    line_1 = raw_content_list[::3]
    line_2 = raw_content_list[1::3]
    line_3 = raw_content_list[2::3]

    rows_tuples = list(zip(line_1, line_2, line_3))
    rows_lists = []

    for row in rows_tuples:
        rows_lists.append(list(row))

    return rows_lists

