from VAR import nation_list


def pdf_with_no_tables_scraper(row_data):
    """
    Pdfs database contains exceptions where pdfplumber cannot find the table. The function takes row data and organizes
    data into rows of information formatted in csv.
    :param row_data: un-formatted data from pdf
    :return: formatted data into csv
    """
    print('pdf with no tables scraper')

    pass


def table_scraper_individual(raw_data):
    """
    Function takes row data from pdfs tables and converts it to csv.
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

        # replace commas if them used instead of dots
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
        for i in row[1].split():
            if i in nation_list:
                nationality_index = row[1].split().index(i)

        # get nationality
        nationality = row[1].split()[nationality_index]

        # get name
        name = ' '.join(row[1].split()[0:nationality_index]).title().replace('.', '')

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

        # replaces spaces and make all values looks the same
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
                gate_jump_1 = row[7].split()[0]
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

        else:
            gate_jump_1 = 'NULL'
            gate_compensation_1 = 'NULL'
            gate_jump_2 = 'NULL'
            gate_compensation_2 = 'NULL'

            wind_jump_1 = 'NULL'
            wind_compensation_1 = 'NULL'
            wind_jump_2 = 'NULL'
            wind_compensation_2 = 'NULL'

        # get jump total points
        total_points_jump_1 = row[-3].split()[0]

        if len(row[-3].split()) == 2:
            total_points_jump_2 = row[-3].split()[1]
        else:
            total_points_jump_2 = 'NULL'

        # get jumps ranking
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

