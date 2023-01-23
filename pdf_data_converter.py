from helpers import find_index
from VAR import nation_list


def text_pdfs_scraper_individual(row_data):
    """
    Pdfs database contains exceptions where pdfplumber cannot find the table. The function takes row data and organizes
    data into rows of information formatted in csv.
    :param row_data: un-formatted data from pdf
    :return: formatted data into csv
    """
    print('pdf with no tables scraper')

    jumpers_data = []

    for row in row_data:

        # reorganise row structure to be consistent
        for i in row[0].split():
            if i in nation_list:
                row = [row[0], row[1], row[2]]

        for i in row[1].split():
            if i in nation_list:
                row = [row[1], row[0], row[2]]

        for i in row[2].split():
            if i in nation_list:
                row = [row[2], row[0], row[1]]

        # handle Man of the Day and missing data in row 1
        if row[0].split()[0] == 'Man' and len(row[1].split()) > 3:
            data_to_move_between_rows = row[0] + ' ' + ' '.join(row[1].split()[1:-1])
            data_for_row_1 = ' '.join(row[1].split()[:1]) + ' ' + row[1].split()[-1]

            row = [data_to_move_between_rows, data_for_row_1, row[2]]

        if len(row[1].split()) == 2:
            if row[0].split()[0] == 'Man':
                row = [row[0][7:], row[1], row[2][8:]]
            else:
                new_row_0 = ' '.join(row[0].split()[:-1])
                new_row_1 = row[1] + ' ' + row[0].split()[-1]

                row = [new_row_0, new_row_1, row[2]]

        # move part of data from row[1] to row[0] to be consistent for all rows
        if len(row[1].split()) != 3:
            data_to_move_between_rows = row[0] + ' ' + ' '.join(row[1].split()[2:-1])
            data_for_row_1 = ' '.join(row[1].split()[:2]) + ' ' + row[1].split()[-1]

            row = [data_to_move_between_rows, data_for_row_1, row[2]]

        # find what row element contains information about nationality like -> NOR
        row_with_nation_element = []
        for element in row:
            element_set = set(element.split())

            d = set(nation_list).intersection(element_set)
            if len(d) == 1:
                row_with_nation_element.append(element)

        # get jumper name, nationality, club
        # get specification of nationality index
        nationality_index = find_index(row_with_nation_element[0].split(), nation_list)

        # get ranking
        ranking = row[1].split()[0].replace('.', '')

        # get nationality
        nationality = row_with_nation_element[0].split()[nationality_index]

        # get name
        name = ' '.join(row[0].split()[0:nationality_index]).title().replace('.', '')

        # clear name data
        if name.split()[0] == 'Man':
            name = ' '.join(name.split()[2:])

        elif name.split()[0] == '*':
            name = ' '.join(name.split()[1:])

        if len(name.split()[0]) <= 2 and len(name.split()[1]) <= 2:
            ranking = name.split()[0]
            name = ' '.join(name.split()[2:])

        # get dob and club
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        month_index = find_index(row[2].split(), months)

        if month_index == 100:
            dob = 'NULL'
            club = 'NULL'
        else:
            dob = ' '.join(row[2].split()[month_index - 1:month_index + 2])
            club = ' '.join(row[2].split()[:month_index - 1])

        # handle missing speed_jump_1 value
        if len(row[0].split()[nationality_index + 1:]) == 10 or len(row[0].split()[nationality_index + 1:]) == 8:
            speed_jump_1 = 'NULL'
            nationality_index = nationality_index - 1
        else:
            speed_jump_1 = row[0].split()[nationality_index + 1]

        # get data for first round
        distance_jump_1 = row[0].split()[nationality_index + 2]
        distance_points_1 = row[0].split()[nationality_index + 3]

        # judge marks for first jump
        judge_marks_jump_1a = row[0].split()[nationality_index + 4]
        judge_marks_jump_1b = row[0].split()[nationality_index + 5]
        judge_marks_jump_1c = row[0].split()[nationality_index + 6]
        judge_marks_jump_1d = row[0].split()[nationality_index + 7]
        judge_marks_jump_1e = row[0].split()[nationality_index + 8]

        judge_total_points_1 = row[0].split()[nationality_index + 9]

        total_points_jump_1 = row[1].split()[-1]
        ranking_jump_1 = row[1].split()[0].replace('.', '')

        # if there is disqualification in second round
        if 'DSQ' in row[2].split():

            gate_jump_1 = 'NULL'
            gate_compensation_1 = 'NULL'
            wind_jump_1 = 'NULL'
            wind_compensation_1 = 'NULL'

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
            ranking_jump_2 = 'DSQ'

        # if there is no second round
        elif len(row[2].split()) < 10:

            gate_jump_1 = 'NULL'
            gate_compensation_1 = 'NULL'
            wind_jump_1 = 'NULL'
            wind_compensation_1 = 'NULL'

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

        else:

            # handle missing speed_jump_2 value
            if len(row[2].split()[month_index + 2:]) == 10:
                speed_jump_2 = 'NULL'
                month_index = month_index - 1

            if len(row[2].split()) == 11 and month_index == 100:
                speed_jump_2 = row[2].split()[0]
                distance_jump_2 = row[2].split()[1]
                distance_points_2 = row[2].split()[2]

                judge_marks_jump_2a = row[2].split()[3]
                judge_marks_jump_2b = row[2].split()[4]
                judge_marks_jump_2c = row[2].split()[5]
                judge_marks_jump_2d = row[2].split()[6]
                judge_marks_jump_2e = row[2].split()[7]

                judge_total_points_2 = row[2].split()[8]
                total_points_jump_2 = row[2].split()[9]
                ranking_jump_2 = row[2].split()[10].replace('.', '')

            else:
                speed_jump_2 = row[2].split()[month_index + 2]
                distance_jump_2 = row[2].split()[month_index + 3]
                distance_points_2 = row[2].split()[month_index + 4]

                judge_marks_jump_2a = row[2].split()[month_index + 5]
                judge_marks_jump_2b = row[2].split()[month_index + 6]
                judge_marks_jump_2c = row[2].split()[month_index + 7]
                judge_marks_jump_2d = row[2].split()[month_index + 8]
                judge_marks_jump_2e = row[2].split()[month_index + 9]

                judge_total_points_2 = row[2].split()[month_index + 10]
                total_points_jump_2 = row[2].split()[month_index + 11]
                ranking_jump_2 = row[2].split()[month_index + 12].replace('.', '')

            gate_jump_1 = 'NULL'
            gate_compensation_1 = 'NULL'
            wind_jump_1 = 'NULL'
            wind_compensation_1 = 'NULL'

            gate_jump_2 = 'NULL'
            gate_compensation_2 = 'NULL'
            wind_jump_2 = 'NULL'
            wind_compensation_2 = 'NULL'

        # get total points
        total_points = row[1].split()[-1]
        team_points = 'NULL'
        team_ranking = 'NULL'

        jumper_row = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1, speed_jump_1,
                      judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c, judge_marks_jump_1d,
                      judge_marks_jump_1e, judge_total_points_1, gate_jump_1, gate_compensation_1, wind_jump_1,
                      wind_compensation_1, total_points_jump_1, ranking_jump_1, distance_jump_2, distance_points_2,
                      speed_jump_2, judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                      judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2, wind_jump_2,
                      wind_compensation_2, total_points_jump_2, ranking_jump_2, total_points, team_points, team_ranking]

        jumpers_data.append(jumper_row)

    return jumpers_data


def table_pdfs_scraper_individual(raw_data):
    """
    Function takes raw data from pdfs tables and converts it to csv.
    :param raw_data: data from pdf tables extracted by pdfplumber
    :return: formatted data into csv
    """
    print('pdf table scraper with tables')

    jumpers_data = []

    for row in raw_data:

        # removing None value from the list
        for i in row:
            if i is None:
                row.remove(i)

        # skip extra None values
        for i in row:
            if i is None:
                row.remove(i)

        for i in row:
            if i is None:
                row.remove(i)

        # replace commas in the string
        row = [i.replace(',', '.') for i in row]

        # get ranking
        if 't' in row[0]:
            row[0] = row[0].split()[0]

        ranking = row[0].replace('.', '')

        # if speed space is empty
        if row[3] == '':
            row[3] = 'NULL'

        # for pdfs with three rounds (skip the qualification round)
        if row[3].split()[0] == 'QuR:' and row[1] == '':
            row[1] = '*'

        # skip if only qualification
        if 'QuR:' in row[3] and '1stR:' not in row[3]:
            break

        # for three rounds if not qualify to second round
        if 'QuR:' in row[3] and '2ndR:' not in row[3]:
            row[3] = row[3].split()[-1]
            row[4] = row[4].split()[-1]
            row[5] = row[5].split()[-1]
            row[6] = row[6].split('\n')[-1]
            row[7] = row[7].split()[-1]
            row[8] = row[8].split('\n')[-1]
            row[9] = row[9].split('\n')[-1]
            row[10] = row[10].split()[-1]
            row[11] = row[11].split()[-1]

        # for three rounds in pdf - skip the qualification round
        if row[3].split()[0] == 'QuR:' and len(row[3].split()) == 6:
            row[3] = row[3].split()[3] + '\n' + row[3].split()[5]
            row[4] = row[4].split()[1] + '\n' + row[4].split()[2]
            row[5] = row[5].split()[1] + '\n' + row[5].split()[2]
            row[6] = row[6].split('\n')[1] + '\n' + row[6].split('\n')[2]
            row[7] = row[7].split()[1] + '\n' + row[7].split()[2]
            row[8] = (row[8].split('\n')[1:][0] + '\n' + row[8].split('\n')[1:][1])
            row[9] = row[9].split('\n')[1] + '\n' + row[9].split('\n')[2]
            row[10] = row[10].split('\n')[1] + '\n' + row[10].split('\n')[2]
            row[11] = row[11].split('\n')[1] + '\n' + row[11].split('\n')[2]

        # skip bib number and 'Man of the Day'
        skip_bib_number = ['*', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'f']

        if len(row[1].split()) > 5 and row[1].split()[0] == 'Man':
            row[1] = row[1][7:]

        if len(row[1]) == 0:
            del row[1]

        if (row[1][0] in skip_bib_number and len(row[1]) in [1, 2, 3, 4, 5]) or row[1].split()[0] == 'Man':
            del row[1]

        if row[1] == 'Man of\nthe Day' or row[1] == 'Man of\nhe Day':
            del row[1]
        if row[1].split()[0][0] in skip_bib_number and row[1].split()[1] != range(0, 9):
            if row[1].split()[0][0] == '*':
                row[1] = row[1][3:].lstrip()
            else:
                row[1] = row[1][2:].lstrip()

        if row[1].split()[0][0] in skip_bib_number and len(row[1].split()[0]) in [1, 2]:
            del row[1]

        # get jumper name, nationality, club
        # get specification of nationality index
        nationality_index = find_index(row[1].split(), nation_list)

        # get name and nationality
        name = ' '.join(row[1].split()[0:nationality_index]).title().replace('.', '')
        nationality = row[1].split()[nationality_index]

        # skip 'Man of the Day'
        if name[0:6] == 'Man Of':
            name = name[7:]

        # get dob and club
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

        if row[1].split()[-2] in months:
            dob = ' '.join(row[1].split()[-3:])
            club = ' '.join(row[1].split()[(nationality_index + 1):-3])

        elif row[1].split()[-1] in nation_list and row[1].split()[-2] not in months:
            dob = 'NULL'
            club = 'NULL'

        elif row[1].split()[-2] not in months:
            dob = 'NULL'
            club = ' '.join(row[1].split()[nationality_index + 1:])

        else:
            dob = 'NULL'
            club = 'NULL'

        if row[1].split()[-2] == months:
            if row[1].split()[-4] == nationality:
                club = 'NULL'

        if club == '':
            club = 'NULL'

        # skip 'Man of the Day'
        if club[0:3] in ['the', 'Day']:
            club = club[4:]

        if club.split()[0][0] in skip_bib_number and len(club.split()[0]) in [1, 2]:
            club = club[2:].lstrip()

        # get speed
        # replace empty string
        if row[2] == '':
            row[2] = row[2].replace('', 'NULL')

        speed_jump_1 = row[2].split()[0]

        if len(row[2].split()) == 2:
            speed_jump_2 = row[2].split()[1]
        else:
            speed_jump_2 = 'NULL'

        # get distance
        distance_jump_1 = row[3].split()[0]

        if len(row[3].split()) == 2:
            distance_jump_2 = row[3].split()[1]
        else:
            distance_jump_2 = 'NULL'

        # get distance points
        distance_points_1 = row[4].split()[0]

        if len(row[4].split()) == 2:
            distance_points_2 = row[4].split()[1]
        else:
            distance_points_2 = 'NULL'

        # get judge marks
        # check if there is disqualification in second jump
        if row[5][-5:] == 'SCE 4' or 'ICR' in row[5] or 'SCE' in row[5]:
            row[5] = row[5].split('\n')[0]

        # replaces space and make all values looks the same
        row[5] = row[5].replace(' ', '')

        if row[5] == 'SCE4' or row[5] == 'SCE1.2.1.1':
            judge_marks_jump_1a = 'NULL'
            judge_marks_jump_1b = 'NULL'
            judge_marks_jump_1c = 'NULL'
            judge_marks_jump_1d = 'NULL'
            judge_marks_jump_1e = 'NULL'

        else:
            judge_marks_jump_1a = row[5].split('\n')[0].split('.')[0] + '.' + \
                                  row[5].split('\n')[0].split('.')[1][0:1]
            judge_marks_jump_1b = row[5].split('\n')[0].split('.')[1][1:] + '.' + \
                                  row[5].split('\n')[0].split('.')[2][0:1]
            judge_marks_jump_1c = row[5].split('\n')[0].split('.')[2][1:] + '.' + \
                                  row[5].split('\n')[0].split('.')[3][0:1]
            judge_marks_jump_1d = row[5].split('\n')[0].split('.')[3][1:] + '.' + \
                                  row[5].split('\n')[0].split('.')[4][0:1]
            judge_marks_jump_1e = row[5].split('\n')[0].split('.')[4][1:] + '.' + \
                                  row[5].split('\n')[0].split('.')[5][0:1]

        if len(row[5].split('\n')) == 2:
            judge_marks_jump_2a = row[5].split('\n')[1].split('.')[0] + '.' + \
                                  row[5].split('\n')[1].split('.')[1][0:1]
            judge_marks_jump_2b = row[5].split('\n')[1].split('.')[1][1:] + '.' + \
                                  row[5].split('\n')[1].split('.')[2][0:1]
            judge_marks_jump_2c = row[5].split('\n')[1].split('.')[2][1:] + '.' + \
                                  row[5].split('\n')[1].split('.')[3][0:1]
            judge_marks_jump_2d = row[5].split('\n')[1].split('.')[3][1:] + '.' + \
                                  row[5].split('\n')[1].split('.')[4][0:1]
            judge_marks_jump_2e = row[5].split('\n')[1].split('.')[4][1:] + '.' + \
                                  row[5].split('\n')[1].split('.')[5][0:1]

        else:
            judge_marks_jump_2a = 'NULL'
            judge_marks_jump_2b = 'NULL'
            judge_marks_jump_2c = 'NULL'
            judge_marks_jump_2d = 'NULL'
            judge_marks_jump_2e = 'NULL'

        # get judge points
        judge_total_points_1 = row[6].split()[0]

        if len(row[6].split()) == 2:
            judge_total_points_2 = row[6].split()[1]
        else:
            judge_total_points_2 = 'NULL'

        # get gate and wind
        gate_jump_1 = 'NULL'
        gate_compensation_1 = 'NULL'
        gate_jump_2 = 'NULL'
        gate_compensation_2 = 'NULL'

        wind_jump_1 = 'NULL'
        wind_compensation_1 = 'NULL'
        wind_jump_2 = 'NULL'
        wind_compensation_2 = 'NULL'

        if len(row) == 10:
            wind_jump_1 = row[8].split()[0]
            if len(row[8].split()) == 2:
                wind_compensation_1 = row[8].split()[1]
            else:
                wind_compensation_1 = 'NULL'
            wind_jump_2 = 'NULL'
            wind_compensation_2 = 'NULL'

            gate_jump_1 = row[7].split()[0].replace('©', '')
            if len(row[7].split()) == 2:
                gate_compensation_1 = row[7].split()[1]
            else:
                gate_compensation_1 = 'NULL'
            gate_jump_2 = 'NULL'
            gate_compensation_2 = 'NULL'

        if row[-5].split() == row[7].split():

            # get wind and wind compensation
            if len(row[8].split()) == 4:
                wind_jump_1 = row[8].split()[0]
                wind_compensation_1 = row[8].split()[1]
                wind_jump_2 = row[8].split()[2]
                wind_compensation_2 = row[8].split()[3]

            else:
                wind_jump_1 = row[8].split()[0]
                wind_compensation_1 = row[8].split()[1]
                wind_jump_2 = 'NULL'
                wind_compensation_2 = 'NULL'

            # get gate and gate compensation
            # for 4 elements
            if len(row[7].split()) == 4:
                gate_jump_1 = row[7].split()[0]
                gate_compensation_1 = row[7].split()[1]
                gate_jump_2 = row[7].split()[2]
                gate_compensation_2 = row[7].split()[3]

            # for 3 elements where second is gate comp
            elif len(row[7].split()) == 3 and '.' in row[7].split()[1]:
                gate_jump_1 = row[7].split()[0]
                gate_compensation_1 = row[7].split()[1]
                gate_jump_2 = row[7].split()[2]
                gate_compensation_2 = 'NULL'

            # for 3 elements where second is gate
            elif len(row[7].split()) == 3 and '.' not in row[7].split()[1]:
                gate_jump_1 = row[7].split()[0]
                gate_compensation_1 = 'NULL'
                gate_jump_2 = row[7].split()[1]
                gate_compensation_2 = row[7].split()[2]

            # for 2 elements where second is gate comp
            elif len(row[7].split()) == 2 and '.' in row[7].split()[1]:
                gate_jump_1 = row[7].split()[0].replace('©', '')
                gate_compensation_1 = row[7].split()[1]
                gate_jump_2 = 'NULL'
                gate_compensation_2 = 'NULL'

            # for 2 elements where second is gate
            elif len(row[7].split()) == 2 and '.' not in row[7].split()[1]:
                gate_jump_1 = row[7].split()[0]
                gate_compensation_1 = 'NULL'
                gate_jump_2 = row[7].split()[1]
                gate_compensation_2 = 'NULL'

            # for 1 element
            elif len(row[7].split()) == 1:
                gate_jump_1 = row[7].split()[0]
                gate_compensation_1 = 'NULL'
                gate_jump_2 = 'NULL'
                gate_compensation_2 = 'NULL'

        # get jump total points
        if len(row) == 8:
            total_points_jump_1 = row[-1]
        else:
            total_points_jump_1 = row[-3].split()[0]

        if len(row[-3].split()) == 2:
            total_points_jump_2 = row[-3].split()[1]
        else:
            total_points_jump_2 = 'NULL'

        if len(row) == 10:
            total_points_jump_1 = row[-1]
            total_points_jump_2 = 'NULL'

        if '-' in total_points_jump_1:
            total_points_jump_1 = total_points_jump_1.split()[0]

        # get jumps ranking
        if len(row) == 8:
            ranking_jump_1 = ranking
        else:
            ranking_jump_1 = row[-2].split()[0].replace('.', '')

        if len(row[-2].split()) == 2:
            ranking_jump_2 = row[-2].split()[1].replace('.', '')
        else:
            ranking_jump_2 = 'NULL'

        # for disqualification in the first round
        if distance_jump_1 == 'DSQ':
            distance_jump_1 = 'NULL'
            ranking_jump_1 = 'DSQ'

        # for disqualification in the second round
        if distance_jump_2 == 'DSQ':
            distance_jump_2 = 'NULL'
            ranking_jump_2 = 'DSQ'

        # get total points
        total_points = row[-1]

        # get team points/ranking
        team_points = 'NULL'
        team_ranking = 'NULL'

        jumper_row = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1, speed_jump_1,
                      judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c, judge_marks_jump_1d,
                      judge_marks_jump_1e, judge_total_points_1, gate_jump_1, gate_compensation_1, wind_jump_1,
                      wind_compensation_1, total_points_jump_1, ranking_jump_1, distance_jump_2, distance_points_2,
                      speed_jump_2, judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                      judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2, wind_jump_2,
                      wind_compensation_2, total_points_jump_2, ranking_jump_2, total_points, team_points, team_ranking]

        jumpers_data.append(jumper_row)

    return jumpers_data


def team_pdf_scraper(data):
    """
    Function takes raw data from team-pdfs tables, pulls and maintain data and converts it to csv.
    :param data: data from pdf tables extracted by pdfplumber
    :return: formatted data into csv
    """
    jumpers_data = []

    for row in data:
        # add club if is included to data
        if row[-1][0].isalpha():
            club = row[-1]
            del row[-1]
        else:
            club = 'NULL'

        # reformat first element of the row list that to be consisted for all competition
        if len(row[0].split()) == 2 and len(row[2].split()) in [1, 2]:
            row_front = ' '.join(row[1].split()[:-1])
            row_end = row[1].split()[-1]
            new_row = [row_front, row[0], row[2], row_end]
            row[0] = ' '.join(new_row)

            del row[2]
            del row[1]

        elif len(row[0].split()) == 2 and len(row[2]) > 3:
            row_front = ' '.join(row[1].split()[:-1])
            row_end = row[1].split()[-1]
            new_row = [row_front, row[0], row_end]
            row[0] = ' '.join(new_row)

            del row[1]

        # for competition that had no second round
        if len(row) == 2:
            row.append('No round two')

        # reformat second and third elements of the row list that to be consisted for all competition
        if row[2] != 'No round two':
            if len(row[1].split()) < 4:
                row[1] = ' '.join([row[2].split()[0], row[1], ' '.join(row[2].split()[1:])])
            else:
                row[1] = row[2] + ' ' + row[1]

            del row[2]

        if len(row) == 2:
            row.append('No round two')

        # get ranking
        ranking = row[0].split()[0].replace('.', '')

        # find nationality
        team_element = [item.replace('(', '').replace(')', '') for item in row[0].split()]
        for el in team_element:
            if el in nation_list:
                nationality = el

        # get team points first-round/second-round/total
        points_list = [i for i in row[0].split() if '.' in i]

        # team_round_1_points = 'NULL'
        # team_round_2_points = 'NULL'
        team_points = 'NULL'
        total_points = 'NULL'

        if len(points_list) == 2:
            # team_round_1_points = points_list[-1]
            # team_round_2_points = 'NULL'
            team_points = points_list[-1]
            total_points = points_list[-1]

        if len(points_list) == 3:
            # team_round_1_points = points_list[0]
            # team_round_2_points = points_list[1]
            team_points = points_list[-1]
            total_points = str("{:.1f}".format(float(points_list[0]) + float(points_list[1])))

        if len(points_list) == 4:
            # team_round_1_points = points_list[-1]
            # team_round_2_points = 'NULL'
            team_points = points_list[-1]
            total_points = points_list[-1]

        if len(points_list) == 5:
            # team_round_1_points = points_list[-1]
            # team_round_2_points = 'NULL'
            team_points = points_list[-1]
            total_points = points_list[-1]

        if len(points_list) == 6:
            # team_round_1_points = points_list[1]
            # team_round_2_points = points_list[3]
            team_points = points_list[-1]
            total_points = str("{:.1f}".format(float(points_list[1]) + float(points_list[3])))

        # replace "," and "."
        if ',' == row[1].split()[1][-1]:
            row[1] = ' '.join([' '.join(row[1].split()[:1]), row[1].split()[1].replace(',', ''),
                               ' '.join(row[1].split()[2:])])

        if ',' == row[1].split()[2][-1] or '.' == row[1].split()[2][-1]:
            row[1] = ' '.join([' '.join(row[1].split()[:2]), row[1].split()[2].replace(',', '').replace('.', ''),
                               ' '.join(row[1].split()[3:])])

        row[1] = row[1].replace(',', '.')

        # handle if there is disqualification in first round
        if any(item in ['DSQ', 'DNS'] for item in row[1].split()) or len(row[1].split()) < 4:
            name = ' '.join(row[1].split()[1:3]).title()
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

        else:
            # get index of last name element
            name_pointer = find_index(row[1].split(), nation_list)
            """
            index_point_list = [i for i in row[1].split()[1:] if '.' in i]
            for i in row[1].split():
                if i == index_point_list[0]:
                    name_end_index_point = row[1].split().index(i)"""

            name = ' '.join(row[1].split()[1:name_pointer]).title().replace(',', '')

            first_round_results = row[1].split()[name_pointer:]

            # if first element is total ranking
            if len(first_round_results) == 8:
                total_points = first_round_results[0]
                first_round_results = first_round_results[1:]

            # judge points handler
            if len(first_round_results[3]) in [3, 4]:
                first_round_results = first_round_results[:3] + [''.join(first_round_results[3:8])] \
                                      + first_round_results[8:]

            if len(first_round_results[3]) == 8:
                first_round_results = first_round_results[:3] + [''.join(first_round_results[3:6])] \
                                      + first_round_results[6:]

            judge_marks_jump_1a = first_round_results[3].split('.')[0] + '.' + \
                                  first_round_results[3].split('.')[1][0:1]

            judge_marks_jump_1b = first_round_results[3].split('.')[1][1:] + '.' + \
                                  first_round_results[3].split('.')[2][0:1]

            judge_marks_jump_1c = first_round_results[3].split('.')[2][1:] + '.' + \
                                  first_round_results[3].split('.')[3][0:1]

            judge_marks_jump_1d = first_round_results[3].split('.')[3][1:] + '.' + \
                                  first_round_results[3].split('.')[4][0:1]

            judge_marks_jump_1e = first_round_results[3].split('.')[4][1:] + '.' +\
                                  first_round_results[3].split('.')[5][0:1]

            if first_round_results[3] == first_round_results[-4]:

                gate_jump_1 = 'NULL'
                gate_compensation_1 = 'NULL'
                wind_jump_1 = 'NULL'
                wind_compensation_1 = 'NULL'

            else:
                gate_wind_data = first_round_results[5:-2]

                # get gate/wind and gate/wind compensation rirst round
                # for 4 elements
                if len(gate_wind_data) == 4:
                    gate_jump_1 = gate_wind_data[0]
                    gate_compensation_1 = gate_wind_data[1]
                    wind_jump_1 = gate_wind_data[2]
                    wind_compensation_1 = gate_wind_data[3]

                # for 3 elements
                elif len(gate_wind_data) == 3:
                    gate_jump_1 = gate_wind_data[0]
                    gate_compensation_1 = 'NULL'
                    wind_jump_1 = gate_wind_data[1]
                    wind_compensation_1 = gate_wind_data[2]

        name = name.replace(' (W)', '').replace(' (M)', '')
        dob = 'NULL'

        distance_jump_1 = first_round_results[1]
        distance_points_1 = first_round_results[2]
        speed_jump_1 = first_round_results[0]
        judge_total_points_1 = first_round_results[4]
        total_points_jump_1 = first_round_results[-2]
        ranking_jump_1 = first_round_results[-1].replace('.', '')

        # second round
        if row[2] in ['0.0', 'No round two']:
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

        else:
            row[2] = row[2].replace(',', '.')

            # if speed 2 element missing
            if len(row[2].split()) == 10:
                row[2] = 'NULL' + ' ' + row[2]

            distance_jump_2 = row[2].split()[1]
            distance_points_2 = row[2].split()[2]
            speed_jump_2 = row[2].split()[0]

            # judge marks handler
            if len(row[2].split()[3]) in [3, 4]:
                row[2] = ' '.join(row[2].split()[:3] + [''.join(row[2].split()[3:8])] + row[2].split()[8:])

            elif len(row[2].split()[3]) == 8:
                row[2] = ' '.join(row[2].split()[:3] + [''.join(row[2].split()[3:6])] + row[2].split()[6:])

            judge_marks_jump_2a = row[2].split()[3].split('.')[0] + '.' + row[2].split()[3].split('.')[1][0:1]
            judge_marks_jump_2b = row[2].split()[3].split('.')[1][1:] + '.' + row[2].split()[3].split('.')[2][0:1]
            judge_marks_jump_2c = row[2].split()[3].split('.')[2][1:] + '.' + row[2].split()[3].split('.')[3][0:1]
            judge_marks_jump_2d = row[2].split()[3].split('.')[3][1:] + '.' + row[2].split()[3].split('.')[4][0:1]
            judge_marks_jump_2e = row[2].split()[3].split('.')[4][1:] + '.' + row[2].split()[3].split('.')[5][0:1]

            if row[2].split()[3] == row[2].split()[-4]:
                gate_jump_2 = 'NULL'
                gate_compensation_2 = 'NULL'
                wind_jump_2 = 'NULL'
                wind_compensation_2 = 'NULL'

            else:
                gate_wind_data = row[2].split()[5:-2]

                if len(gate_wind_data) == 4:
                    gate_jump_2 = gate_wind_data[0]
                    gate_compensation_2 = gate_wind_data[1]
                    wind_jump_2 = gate_wind_data[2]
                    wind_compensation_2 = gate_wind_data[3]
                else:
                    gate_jump_2 = gate_wind_data[0]
                    gate_compensation_2 = 'NULL'
                    wind_jump_2 = gate_wind_data[1]
                    wind_compensation_2 = gate_wind_data[2]

            judge_total_points_2 = row[2].split()[4]
            total_points_jump_2 = row[2].split()[-2]
            ranking_jump_2 = row[2].split()[-1].replace('.', '')
        team_ranking = ranking

        jumper_row = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1, speed_jump_1,
                      judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c, judge_marks_jump_1d,
                      judge_marks_jump_1e, judge_total_points_1, gate_jump_1, gate_compensation_1, wind_jump_1,
                      wind_compensation_1, total_points_jump_1, ranking_jump_1, distance_jump_2, distance_points_2,
                      speed_jump_2, judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                      judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2, wind_jump_2,
                      wind_compensation_2, total_points_jump_2, ranking_jump_2, total_points, team_points, team_ranking]

        jumpers_data.append(jumper_row)

    return jumpers_data
