import textwrap
from helpers import disqualification_check


def pdf_with_no_tables_scraper(row_data):
    """
    Pdfs database contains exceptions where pdfplumber cannot find the table. The function takes row data and organizes
    data into rows of information formatted in csv.
    :param row_data: un-formatted data from pdf
    :return: formatted data into csv
    """
    print('pdf with no tables scraper')

    jumpers_rows = []

    # data list length counter
    n = int(len(row_data) / 3)

    # jumper raw data list of lists creator
    jumper_content = []

    # jumper list line creator (from raw data to csv)
    for _ in range(n):
        jumper_row_list = [row_data[0], row_data[1], row_data[2]]
        jumper_content.append(jumper_row_list)
        del row_data[0:3]

    # jumper csv row data creator
    for row in jumper_content:

        # clear 'Man of the Day' from row
        if row[0][0].split()[0] == 'Man':
            row = [[' '.join(row[0][0].split()[2:])], row[1], [' '.join(row[2][0].split()[2:])]]

        # check if DSQ row exists and create csv data row
        if 'SCE' in row[0][0].split():
            for element in row:
                for el in element:

                    # skip elements
                    if el.split()[0] == 'Reason' or el.split()[0] == 'SCE':
                        continue

                    # skip last two elements
                    if el.split()[-2] == 'SCE':

                        name = ' '.join(el.split()[1:-3]).title()
                        nationality = el.split()[-3]

                    else:
                        name = ' '.join(el.split()[1:-1]).title()
                        nationality = el.split()[-1]

                    ranking = 'DSQ'
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
                    total_points = 'NULL'
                    team_points = 'NULL'
                    team_ranking = 'NULL'

                    jumper_line = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1,
                                   speed_jump_1, judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c,
                                   judge_marks_jump_1d, judge_marks_jump_1e, judge_total_points_1, gate_jump_1,
                                   gate_compensation_1, wind_jump_1, wind_compensation_1, total_points_jump_1,
                                   ranking_jump_1, distance_jump_2, distance_points_2, speed_jump_2,
                                   judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                                   judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2,
                                   wind_jump_2, wind_compensation_2, total_points_jump_2, ranking_jump_2,
                                   total_points, team_points, team_ranking]

                    jumpers_rows.append(jumper_line)

        # no tables and only one round
        elif len(row[1][0].split()) == 11:

            ranking = row[1][0].split()[0].replace('.', '')
            name = ' '.join(row[0][0].split()[:-1]).title()
            nationality = row[0][0].split()[-1]

            dob = ' '.join(row[2][0].split()[-3:])
            club = ' '.join(row[2][0].split()[:-3])

            speed_jump_1 = row[1][0].split()[1]
            speed_jump_2 = 'NULL'

            distance_jump_1 = row[1][0].split()[2]
            distance_jump_2 = 'NULL'

            ranking_jump_1 = ranking
            ranking_jump_2 = 'NULL'

            distance_points_1 = row[1][0].split()[3]
            distance_points_2 = 'NULL'

            judge_marks_jump_1a = row[1][0].split()[4]
            judge_marks_jump_1b = row[1][0].split()[5]
            judge_marks_jump_1c = row[1][0].split()[6]
            judge_marks_jump_1d = row[1][0].split()[7]
            judge_marks_jump_1e = row[1][0].split()[8]

            judge_marks_jump_2a = 'NULL'
            judge_marks_jump_2b = 'NULL'
            judge_marks_jump_2c = 'NULL'
            judge_marks_jump_2d = 'NULL'
            judge_marks_jump_2e = 'NULL'

            gate_jump_1 = 'NULL'
            gate_compensation_1 = 'NULL'
            wind_jump_1 = 'NULL'
            wind_compensation_1 = 'NULL'

            gate_jump_2 = 'NULL'
            gate_compensation_2 = 'NULL'
            wind_jump_2 = 'NULL'
            wind_compensation_2 = 'NULL'

            judge_total_points_1 = row[1][0].split()[9]
            judge_total_points_2 = 'NULL'

            total_points_jump_1 = row[1][0].split()[10]
            total_points_jump_2 = 'NULL'

            total_points = row[1][0].split()[10]

            team_points = 'NULL'
            team_ranking = 'NULL'

            jumper_line = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1,
                           speed_jump_1, judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c,
                           judge_marks_jump_1d, judge_marks_jump_1e, judge_total_points_1, gate_jump_1,
                           gate_compensation_1, wind_jump_1, wind_compensation_1, total_points_jump_1,
                           ranking_jump_1, distance_jump_2, distance_points_2, speed_jump_2,
                           judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                           judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2,
                           wind_jump_2, wind_compensation_2, total_points_jump_2, ranking_jump_2,
                           total_points, team_points, team_ranking]

        elif len(row[0][0].split()) <= 6:

            ranking = row[1][0].split()[0].replace('.', '')
            name = ' '.join(row[0][0].split()[:-1]).title()
            nationality = row[0][0].split()[-1]

            dob = ' '.join(row[2][0].split()[-3:])
            club = ' '.join(row[2][0].split()[:-3])

            speed_jump_1 = row[1][0].split()[2]
            speed_jump_2 = 'NULL'

            distance_jump_1 = row[1][0].split()[3]
            distance_jump_2 = 'NULL'

            ranking_jump_1 = ranking
            ranking_jump_2 = 'NULL'

            distance_points_1 = row[1][0].split()[4]
            distance_points_2 = 'NULL'

            judge_marks_jump_1a = row[1][0].split()[5]
            judge_marks_jump_1b = row[1][0].split()[6]
            judge_marks_jump_1c = row[1][0].split()[7]
            judge_marks_jump_1d = row[1][0].split()[8]
            judge_marks_jump_1e = row[1][0].split()[9]

            judge_marks_jump_2a = 'NULL'
            judge_marks_jump_2b = 'NULL'
            judge_marks_jump_2c = 'NULL'
            judge_marks_jump_2d = 'NULL'
            judge_marks_jump_2e = 'NULL'

            gate_jump_1 = 'NULL'
            gate_compensation_1 = 'NULL'
            wind_jump_1 = 'NULL'
            wind_compensation_1 = 'NULL'

            gate_jump_2 = 'NULL'
            gate_compensation_2 = 'NULL'
            wind_jump_2 = 'NULL'
            wind_compensation_2 = 'NULL'

            judge_total_points_1 = row[1][0].split()[10]
            judge_total_points_2 = 'NULL'

            total_points_jump_1 = row[1][0].split()[11]
            total_points_jump_2 = 'NULL'

            total_points = row[1][0].split()[11]

            team_points = 'NULL'
            team_ranking = 'NULL'

            jumper_line = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1,
                           speed_jump_1, judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c,
                           judge_marks_jump_1d, judge_marks_jump_1e, judge_total_points_1, gate_jump_1,
                           gate_compensation_1, wind_jump_1, wind_compensation_1, total_points_jump_1,
                           ranking_jump_1, distance_jump_2, distance_points_2, speed_jump_2,
                           judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                           judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2,
                           wind_jump_2, wind_compensation_2, total_points_jump_2, ranking_jump_2,
                           total_points, team_points, team_ranking]

        elif len(row[0][0].split()) == 11:

            ranking = row[1][0].split()[0]
            name = ' '.join(row[1][0].split()[2:-2]).title()
            nationality = row[1][0].split()[-2]
            dob = 'NULL'
            club = 'NULL'

            speed_jump_1 = row[0][0].split()[0]
            distance_jump_1 = row[0][0].split()[1]
            distance_points_1 = row[0][0].split()[3]

            judge_marks_jump_1a = row[0][0].split()[3]
            judge_marks_jump_1b = row[0][0].split()[4]
            judge_marks_jump_1c = row[0][0].split()[5]
            judge_marks_jump_1d = row[0][0].split()[6]
            judge_marks_jump_1e = row[0][0].split()[7]

            judge_total_points_1 = row[0][0].split()[8]
            total_points_jump_1 = row[0][0].split()[9]
            ranking_jump_1 = row[0][0].split()[10]

            speed_jump_2 = row[2][0].split()[0]
            distance_jump_2 = row[2][0].split()[1]
            distance_points_2 = row[2][0].split()[3]

            judge_marks_jump_2a = row[2][0].split()[3]
            judge_marks_jump_2b = row[2][0].split()[4]
            judge_marks_jump_2c = row[2][0].split()[5]
            judge_marks_jump_2d = row[2][0].split()[6]
            judge_marks_jump_2e = row[2][0].split()[7]

            gate_jump_1 = 'NULL'
            gate_compensation_1 = 'NULL'
            wind_jump_1 = 'NULL'
            wind_compensation_1 = 'NULL'

            gate_jump_2 = 'NULL'
            gate_compensation_2 = 'NULL'
            wind_jump_2 = 'NULL'
            wind_compensation_2 = 'NULL'

            judge_total_points_2 = row[2][0].split()[8]
            total_points_jump_2 = row[2][0].split()[9]
            ranking_jump_2 = row[2][0].split()[10]

            total_points = row[1][0].split()[-1]

            team_points = 'NULL'
            team_ranking = 'NULL'

            jumper_line = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1,
                           speed_jump_1, judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c,
                           judge_marks_jump_1d, judge_marks_jump_1e, judge_total_points_1, gate_jump_1,
                           gate_compensation_1, wind_jump_1, wind_compensation_1, total_points_jump_1,
                           ranking_jump_1, distance_jump_2, distance_points_2, speed_jump_2,
                           judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                           judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2,
                           wind_jump_2, wind_compensation_2, total_points_jump_2, ranking_jump_2,
                           total_points, team_points, team_ranking]

        else:
            # clear 'Man of the Day' from row
            if row[0][0].split()[0] == 'Man':
                row = [[' '.join(row[0][0].split()[2:])], row[1], [' '.join(row[2][0].split()[2:])]]

            ranking = row[1][0].split()[0].replace('.', '')
            name = ' '.join(row[0][0].split()[:-12]).title()
            nationality = row[0][0].split()[-12]

            speed_jump_1 = row[0][0].split()[-11]
            distance_jump_1 = row[0][0].split()[-10]
            distance_points_1 = row[0][0].split()[-9]

            judge_marks_jump_1a = row[0][0].split()[-8]
            judge_marks_jump_1b = row[0][0].split()[-7]
            judge_marks_jump_1c = row[0][0].split()[-6]
            judge_marks_jump_1d = row[0][0].split()[-5]
            judge_marks_jump_1e = row[0][0].split()[-4]

            gate_jump_1 = 'NULL'
            gate_compensation_1 = 'NULL'
            wind_jump_1 = 'NULL'
            wind_compensation_1 = 'NULL'

            gate_jump_2 = 'NULL'
            gate_compensation_2 = 'NULL'
            wind_jump_2 = 'NULL'
            wind_compensation_2 = 'NULL'

            judge_total_points_1 = row[0][0].split()[-3]
            total_points_jump_1 = row[0][0].split()[-2]

            ranking_jump_1 = row[0][0].split()[-1].replace('.', '')

            if len(row[2][0].split()) > 11:
                club = ' '.join(row[2][0].split()[:-14])
                date_list = row[2][0].split()[-14:-11]
                dob = ' '.join(date_list)

                judge_marks_jump_2a = row[2][0].split()[-8]
                judge_marks_jump_2b = row[2][0].split()[-7]
                judge_marks_jump_2c = row[2][0].split()[-6]
                judge_marks_jump_2d = row[2][0].split()[-5]
                judge_marks_jump_2e = row[2][0].split()[-4]

                judge_total_points_2 = row[2][0].split()[-3]

                total_points_jump_2 = row[2][0].split()[-2]
                ranking_jump_2 = row[2][0].split()[-1]

                speed_jump_2 = row[2][0].split()[-11]
                distance_jump_2 = row[2][0].split()[-10]
                distance_points_2 = row[2][0].split()[-9]

            else:
                club = ' '.join(row[2][0].split())
                date_list = row[2][0].split()[-3:]
                dob = ' '.join(date_list)

                judge_marks_jump_2a = 'NULL'
                judge_marks_jump_2b = 'NULL'
                judge_marks_jump_2c = 'NULL'
                judge_marks_jump_2d = 'NULL'
                judge_marks_jump_2e = 'NULL'

                judge_total_points_2 = 'NULL'

                total_points_jump_2 = 'NULL'

                if row[2][0].split()[-4] == 'DSQ':
                    ranking_jump_2 = 'DSQ'

                else:
                    ranking_jump_2 = 'NULL'

                speed_jump_2 = 'NULL'
                distance_jump_2 = 'NULL'
                distance_points_2 = 'NULL'

            total_points = row[1][0].split()[-1]
            team_points = 'NULL'
            team_ranking = 'NULL'

            jumper_line = [ranking, name, nationality, dob, club, distance_jump_1, distance_points_1,
                           speed_jump_1, judge_marks_jump_1a, judge_marks_jump_1b, judge_marks_jump_1c,
                           judge_marks_jump_1d, judge_marks_jump_1e, judge_total_points_1, gate_jump_1,
                           gate_compensation_1, wind_jump_1, wind_compensation_1, total_points_jump_1,
                           ranking_jump_1, distance_jump_2, distance_points_2, speed_jump_2,
                           judge_marks_jump_2a, judge_marks_jump_2b, judge_marks_jump_2c, judge_marks_jump_2d,
                           judge_marks_jump_2e, judge_total_points_2, gate_jump_2, gate_compensation_2,
                           wind_jump_2, wind_compensation_2, total_points_jump_2, ranking_jump_2,
                           total_points, team_points, team_ranking]

    jumpers_rows.append(jumper_line)

    """for i in jumpers_rows:
        print(i)"""

    return jumpers_rows


def table_scraper_individual(raw_data):
    """
    Function takes row data from pdfs tables and converts it to csv.
    :param raw_data: data from pdf tables extracted by pdfplumber
    :return: formatted data into csv
    """
    print('pdf table scraper with tables')

    pass
