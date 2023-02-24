import os
import shutil


def season(csv_name):
    """
    Function checks and creates a season date, is taking information from file name.
    :param csv_name: csv file name
    :return: season date (format: 2011-2012)
    """

    season_year = csv_name[0:4]

    if csv_name[-13:-11] in ['CH', 'OL', "GP"]:
        season_date = season_year
    elif csv_name[5:7] in ["10", "11", "12"]:
        season_date = f"{season_year}-{int(season_year) + 1}"
    elif csv_name[5:7] in ["01", "02", "03", "04", "05"]:
        season_date = f"{int(season_year) - 1}-{season_year}"
    else:
        season_date = season_year

    return season_date


def location_check(csv_name):
    """
    Function creates path for giving csv file (based on csv file name)
    :param csv_name: csv file name
    :return: path where to save giving file
    """
    csv_name = str(csv_name)

    tournament_type = csv_name[-13:-11]
    tournament_gender = csv_name[-7]
    team_individual = csv_name[-5]

    if tournament_gender == 'M':
        gender = 'Man'
    elif tournament_gender == 'W':
        gender = 'Women'
    elif tournament_gender == 'X':
        gender = 'Mixed'
    else:
        gender = '?'
        print("Something went wrong - gender: " + tournament_gender)

    if "WC" == tournament_type:
        type_tour = 'World Cup'
    elif "GP" == tournament_type:
        type_tour = "Grand Prix"
    elif "OL" == tournament_type:
        type_tour = 'Olympics'
    elif "CH" == tournament_type:
        type_tour = 'World Championship'
    else:
        type_tour = "?"
        print("Something went wrong - tournament type: " + tournament_type)

    if "I" == team_individual:
        team_ind = 'Individual'
    elif "T" == team_individual:
        team_ind = 'Team'
    else:
        team_ind = "?"
        print("Something went wrong - team/ind: " + team_individual)

    # location / path where the file will be save
    location = f"/Users/pik/Desktop/SKI_DB/{gender}/{type_tour}/{team_ind}/"

    return location


def creating_db(src):
    """
    Function saves csv files to the right folders (created them if no exists).
    Taking information from location_check and season function.
    :param src: source path to directory with all csv files
    """

    for file in os.listdir(src):
        if file.endswith(".csv"):

            try:
                os.makedirs(location_check(file) + "/" + season(file))
                print(f'Folder Created: {season(file)}')
            except FileExistsError:
                print(f'Folder already exists: {season(file)}')
            shutil.copy(src + "/" + file, (location_check(file) + "/" + season(file) + "/" + file))

        if file.endswith(".csv") or file.endswith(".pdf"):
            os.remove(file)
