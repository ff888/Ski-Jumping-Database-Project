import datetime as dt
import requests
import pandas as pd

from operator import itemgetter
from VAR import HEADERS


def file_name_creator(soup, cod):
    """
    Function checks fis web and creates a file name using scraped information from there.
    Name structure: Year-Month-Day_City_TournamentType_HillSize_Gender_Team/Individual (2018-Mar-25_Oberstdorf(GER)_WC_NH_W_I)
    :param soup: web parser by BeautifulSoup (soup)
    :param cod: fis codex number
    :return: file name as a string
    """

    # city name where the tournament held
    city = soup.h1.text.replace(' ', '').replace('/', '')

    if ',' in city:
        city = city.split(',')[0] + city.split(',')[1][2:]

    # gender and type of tournament check
    info_line = soup.find('div', class_='event-header__kind').text

    if "Men's Team" in info_line or info_line.split()[1] == 'Team':
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
            else:
                hill = '??'
                print('Hill size not defined: ', info_line)

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
        else:
            hill = '??'
            print('Hill size not defined: ', info_line)

    # type of the tournament
    tournament_type = soup.find('div', class_='event-header__subtitle').text

    if tournament_type in ['World Cup', 'Viessmann FIS Ski Jumping World Cup']:
        short_tournament_type = 'WC'
    elif tournament_type in ['World Championships', 'World Ski Championships']:
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


def disqualification_row_handler(data):
    """
    Creates rows for disqualification jumpers.
    :param data:
    :return:
    """
    pass


def team_points_creator(data):
    """
    Calculates and adds two columns to data: team_points and team_ranking.

    :return: DataFrame updated with two columns team_points and team_ranking
    """

    df = pd.DataFrame(data)
    # pd.set_option('display.max_columns', None)
    df.columns = HEADERS

    df_team = df[['NATIONALITY', 'TOTAL POINTS JUMP 1', 'TOTAL POINTS JUMP 2', 'TEAM POINTS']]

    # if jump2points value is NULL replace by value from jump1points
    df_team['TOTAL POINTS JUMP 2'].mask(df_team['TOTAL POINTS JUMP 2'] == 'NULL',
                                        df_team['TOTAL POINTS JUMP 1'], inplace=True)

    # check if there was only one round, if so set jump_2 0.0 points
    valid_jump_1 = df_team.loc[0, 'TOTAL POINTS JUMP 2']
    if valid_jump_1 == 'NULL':
        df_team['TOTAL POINTS JUMP 2'].mask(df['TOTAL POINTS JUMP 2'] == 'NULL', 0.0, inplace=True)

    # check if jumper was DNS in any of round
    df_team['TOTAL POINTS JUMP 1'].mask(df_team['TOTAL POINTS JUMP 1'] == 'DNS', 0.0, inplace=True)
    df_team['TOTAL POINTS JUMP 1'].mask(df_team['TOTAL POINTS JUMP 1'] == 'DSQ', 0.0, inplace=True)

    df_team['TOTAL POINTS JUMP 2'].mask(df_team['TOTAL POINTS JUMP 2'] == 'DNS', 0.0, inplace=True)
    df_team['TOTAL POINTS JUMP 2'].mask(df_team['TOTAL POINTS JUMP 2'] == 'DSQ', 0.0, inplace=True)

    # add jump1 and jump2 and add JUMP_ADDED column to df_team table
    df_team['TOTAL POINTS JUMP 1'] = df_team['TOTAL POINTS JUMP 1'].str.replace(',', '.').astype(float)
    df_team['TOTAL POINTS JUMP 2'] = df_team['TOTAL POINTS JUMP 2'].str.replace(',', '.').astype(float)

    df_team['JUMPS_ADDED'] = df_team['TOTAL POINTS JUMP 1'] + df_team['TOTAL POINTS JUMP 2']
    # print(df_team)

    # list of teams in the competition
    nation = df_team['NATIONALITY']
    nation_no_dup_list = nation.drop_duplicates().tolist()

    # choose 4 top jumpers from each team and add points, create list with lists [[nationality, team_points],...]
    team_and_points = []
    for i in nation_no_dup_list:
        filter_by_nationality = (nation == i)
        team = df_team[filter_by_nationality]

        top_4 = team.nlargest(4, 'JUMPS_ADDED')  # select top 4 jumpers
        sum_top_4 = top_4['JUMPS_ADDED'].sum()  # add top jumpers points

        team_points = (float("{:.1f}".format(sum_top_4)))
        team_and_points.append([i, team_points])

    # sort list - descending
    sort_points = sorted(team_and_points, key=itemgetter(1), reverse=True)

    # add ranking
    for n in range(1, len(sort_points) + 1):
        sort_points[n - 1].append(n)

    # create df table with 3 columns
    df_list = pd.DataFrame(sort_points, columns=['NATIONALITY', 'TEAM POINTS', 'TEAM RANKING'])

    # marge original table with df_list table
    df.drop(columns=['TEAM POINTS', 'TEAM RANKING'], inplace=True)
    df_data = pd.merge(df, df_list, how='left', left_on='NATIONALITY', right_on='NATIONALITY')

    return df_data


def clear_tables(data):
    """
    Function clears table if rows are not valid (da not hold jumper data).

    :param data: raw data from the pdf tables
    :return: cleared raw data
    """

    table_raw_content_list = []

    # clean rows for pdfs with tables
    data_to_skip = ['Jury', 'RACE', 'Club', 'Rank', 'Name', 'Fini', 'not ', 'Disq', 'Code', 'PRAG', 'NOC ',
                    'Not ', 'TIME', 'WIND', 'Fina', 'GATE', 'No. D', 'Comp', 'Worl', 'FIS ', 'Hill']

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
                if row[0][0:4] in ['Note', 'NOTE']:
                    break

                # DSQ row
                if row[0] == '1st Round':
                    continue
                if row[0] == '' or row[0].split()[0] in ['DNS', 'DSQ']:
                    continue
                if 'SCE' in row or 'ICR' in row[2] or 'SCE' in row[2]:
                    continue
                if row[1] == '':
                    continue
                if row[3] == 'Final':
                    continue

                table_raw_content_list.append(row)

    return table_raw_content_list


def clear_text(data):
    """
    Function clears table if rows are not valid (da not hold jumpers data).
    :param data: raw data pulled from pdf
    :return: list of jumpers rows
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

            # DSQ row
            if 'SCE 4' in row and 'DSQ' not in row:
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


def clear_team_text(data):
    """
    Function clears table if rows are not valid (do not hold jumpers data), for team and mixed competition only.
    :param data: data pulled from team-pdfs
    :return: list of jumpers rows
    """

    data_to_skip = ['Assistant', '"ruhrgas"', 'Ski-Jumping', 'Official', 'Finish', 'Jury', 'Race', 'Technical',
                    'created', 'Nat', 'Rank', 'Name', '[km/h]', 'FIS', 'Print', 'Chief', 'Unofficial', 'SKI', 'SAUT',
                    'Page', 'qualified', 'RESULTS', 'TEAM', 'K120', 'UTAH', 'NOC', 'Report:', 'End', 'Results',
                    'Centre', 'Willingen', '"e.on', 'presented', 'Wisla', 'Final', 'Hinterzarten', 'Rasnov', 'Ljubno',
                    'Zao', 'Titisee-Neustadt', 'Ruka', 'Harrachov', 'Planica', 'Kuopio', 'Klingenthal', 'Timing',
                    'Oslo', 'Lahti', 'Start', 'Fiemme', 'Team', 'FIS', 'timing', 'Ljubno', 'Chaikovsky', 'Pragelato',
                    'SEEFELD/TIROL', 'Oberstdorf', 'Chaikovsky', 'Courchevel', 'Zakopane', 'Competition', 'ÉQUIPE',
                    'provided', 'Report', 'Falun', 'Sapporo', 'Klingenthal', 'Jumping', 'Equipment', 'Not', 'Kuusamo',
                    'ski.com', 'Vikersund', 'Speed', 'Liberec', 'TIME', '/', 'TECHNICAL', 'EQUIPMENT', 'CORRECTION',
                    'NSA', 'www.fisskijumping.com', 'www.fis-ski.com', 'Lillehammer', 'Комплекс', 'Complexe',
                    'Командный', 'Итоговые', 'MON', 'MANCHE FINALE', 'FINAL', 'MANCHE', 'SAT'
                    ]

    clean_lines_list = []
    index_list = []

    for rows in data:
        for row in rows.split('\n'):

            # skip not valid rows
            if row.split()[0][0] == '(':
                continue
            if any(item in row.split() for item in data_to_skip):
                continue
            if row.split()[0] == 'SCE':
                disqualification_row_handler(row)
            if '12:12' in row.split() and 'NOV' in row.split():  # 3337
                continue

            # end when its reach end of the table (valid data)
            if row.split()[0] in ['Data', 'Technical', 'Weather', 'Reason', 'Time', 'Base', 'WIND', 'Temp.']:
                break

            clean_lines_list.append(row)

    line_check = []
    # creates two list to handle data in different way (list 1: 1-8 places, list 2: 9+ places)
    for line in clean_lines_list:

        # list helper to find 9th place
        line_check.append(line.split()[0])

        # for 1-8 places and no second round, no places 9+
        if any(item in ['9', '9.'] for item in line_check) is False:
            three_elements_list = clean_lines_list
            two_elements_list = []

        # find 9th place index include double 9th places scenario
        if line.split()[0] == '9.' or line.split()[0] == '9':

            i = clean_lines_list.index(line)
            index_list.append(i)

            index = min(index_list)

            if len(clean_lines_list[index - 1].split()) == 2:
                three_elements_list = clean_lines_list[:index - 1]
                two_elements_list = clean_lines_list[index - 1:]

            else:
                three_elements_list = clean_lines_list[:index]
                two_elements_list = clean_lines_list[index:]

    # handle problem with formatting, missing element - club
    if len(two_elements_list) != 0:
        if two_elements_list[0][0].isalpha():
            el = two_elements_list[0]

            three_elements_list.append(el)
            two_elements_list = two_elements_list[1:]

    # handle three elements row (teams that qualified to second round)
    pre_jumper_line = []
    if len(three_elements_list[0].split()) == 2 and len(three_elements_list[2].split()) == 2:

        while len(three_elements_list) != 0:
            pre_jumper_line.append(three_elements_list[0:3])

            del three_elements_list[0:3]

    elif '-' in three_elements_list[1].split()[0] and '-' in three_elements_list[4].split()[0]:

        for i in three_elements_list:
            pre_jumper_line.append([i])

    else:
        # find team index
        team_index_list = []
        for i in three_elements_list:
            if '.' in i[:3]:
                index = three_elements_list.index(i)
                team_index_list.append(index)

        # divide teams in separate list
        team_list_data = []
        while len(team_index_list) != 1:

            team_chunk = []
            for i in three_elements_list[team_index_list[0]:team_index_list[1]]:
                team_chunk.append(i)

            del team_index_list[0]
            team_list_data.append(team_chunk)

        pre_jumper_line = []
        for team_row in team_list_data:
            team_info = team_row[0]

            pre_jumper_line.append([team_info])

            jumpers_row = team_row[1:]

            while len(jumpers_row) != 0:
                if len(jumpers_row) <= 3:
                    pre_jumper_line.append(jumpers_row)
                    break

                elif '-' in jumpers_row[3].split()[0]:
                    pre_jumper_line.append(jumpers_row[:2])
                    del jumpers_row[0:2]

                else:
                    pre_jumper_line.append(jumpers_row[:3])
                    del jumpers_row[0:3]

    # handle two elements row (teams that not qualified to second round)
    if len(two_elements_list) == 0:
        pass

    elif '-' in two_elements_list[1].split()[0] and '-' in two_elements_list[1].split()[0]:
        for i in two_elements_list:
            pre_jumper_line.append([i])

    elif len(two_elements_list[0].split()) == 2 and '-' in two_elements_list[4].split()[0]:
        while len(two_elements_list) != 0:
            pre_jumper_line.append(two_elements_list[0:3])

            del two_elements_list[0:3]

    elif len(two_elements_list[0].split()) == 2 and '-' in two_elements_list[3].split()[0]:
        while len(two_elements_list) != 0:
            pre_jumper_line.append(two_elements_list[0:2])

            del two_elements_list[0:2]

    # create jumper row
    jumpers_line = []
    while len(pre_jumper_line) != 0:
        data_chunk = pre_jumper_line[0:5]

        jumper_1 = data_chunk[0] + data_chunk[1]
        jumper_2 = data_chunk[0] + data_chunk[2]
        jumper_3 = data_chunk[0] + data_chunk[3]
        jumper_4 = data_chunk[0] + data_chunk[4]

        jumpers_line.append(jumper_1)
        jumpers_line.append(jumper_2)
        jumpers_line.append(jumper_3)
        jumpers_line.append(jumper_4)

        del pre_jumper_line[0:5]

    return jumpers_line


def find_index(data_row, compare_list):
    """
    It is comparing two list if it finds the same element in both lists will return index of the element in first list.
    :param data_row: list of elements from given data row
    :param compare_list: list of elements that be compared to data_row
    :return: index nuber
    """

    count_elements = []  # append elements only before nation element
    for i in data_row:
        if i not in compare_list:
            count_elements.append(i)
        else:

            break

    index_number = len(count_elements)
    if len(data_row) == len(count_elements):
        index_number = 100

    return index_number
