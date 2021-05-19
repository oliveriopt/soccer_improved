from src.utils.get_root_path import get_project_root
from src.utils.measure_time import measure_time
from src.define_paths import define_path

import src.cons_paths as cons_path
import src.cons_input_data as cons_input
import pandas as pd
import csv

pd.set_option('display.max_rows', 500000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


### CREATE THE DYNAMICA RATING WITH ONLY POINTS FOR EVERY INDICATOR

class CreateDynamicsPoints:

    def __init__(self, league: str):
        self.path = str(get_project_root())
        self.path_dict = define_path(league=league)
        self.stats = pd.DataFrame()
        self.teams = pd.DataFrame()
        self.data_team_total = pd.DataFrame()
        self.data_team_home = pd.DataFrame()
        self.data_team_away = pd.DataFrame()
        self.list_rating = []
        self.output = None

    def __select_data_team(self, team: str) -> pd.DataFrame:
        """
        Create dataframe with the team stats for a year
        :return:
        """
        self.data_team_home = self.stats.loc[self.stats[cons_input.home_team] == team].sort_values(
            by="Date").reset_index(drop=True)
        self.data_team_away = self.stats.loc[self.stats[cons_input.away_team] == team].sort_values(
            by="Date").reset_index(drop=True)
        self.data_team_total = self.data_team_home.append(self.data_team_away).sort_values(
            by="Date").reset_index(drop=True)

    def __read_file(self, year: int) -> None:
        """
        Read the file with the odds and stats
        :param year:
        :return:
        """
        self.stats = pd.read_csv(self.path + self.path_dict.get("path_odds_stats") + cons_path.stats + str(year) +
                                 cons_path.csv,
                                 sep=",",
                                 encoding='unicode_escape', index_col=0)
        self.stats['Date'] = pd.to_datetime(self.stats['Date'].astype(str), format='%Y-%m-%d')

    def __read_teams(self):
        """
        Read teams file and convert into dataframe
        :param year:
        :return:
        """
        self.teams = pd.read_csv(self.path + self.path_dict.get("path_teams") + cons_path.teams + cons_path.csv,
                                 sep=",",
                                 encoding='unicode_escape', index_col=0)

    def __write_file(self, year: int) -> None:
        """
        Write file to the folder 0X_rating_dynamic
        :param year: year to analyze
        :return:
        """
        self.output.to_csv(self.path + self.path_dict.get("path_rating_dynamic") + cons_path.rating_dynamic +
                           "_" + str(year) + cons_path.csv, index=False)

    def __calculate_rating(self, team: str, year: int) -> list:
        """
        Calculate rating for all indicators
        :param team: team
        :param year: year
        :return:
        """

        for type_rating in cons_input.type_rating_dynamic[:]:
            for index, row in self.data_team_home.iterrows():
                if type_rating == "dynamic_ft_home":
                    if row['FTHG'] > row['FTAG']:
                        points = 3
                    elif row['FTHG'] == row['FTAG']:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_home_g>15":
                    if (row['FTHG'] + row['FTAG']) > 1.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_home_g>25":
                    if (row['FTHG'] + row['FTAG']) > 2.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_home_g>35":
                    if (row['FTHG'] + row['FTAG']) > 3.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_home_g<15":
                    if (row['FTHG'] + row['FTAG']) < 1.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_home_g<25":
                    if (row['FTHG'] + row['FTAG']) < 2.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_home_g<35":
                    if (row['FTHG'] + row['FTAG']) < 3.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])

                if type_rating == "dynamic_ht_home":
                    if row['HTHG'] > row['HTAG']:
                        points = 3
                    elif row['HTHG'] == row['HTAG']:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_home_g>15":
                    if (row['HTHG'] + row['HTAG']) > 1.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_home_g>25":
                    if (row['HTHG'] + row['HTAG']) > 2.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_home_g>35":
                    if (row['HTHG'] + row['HTAG']) > 3.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_home_g<15":
                    if (row['HTHG'] + row['HTAG']) < 1.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_home_g<25":
                    if (row['HTHG'] + row['HTAG']) < 2.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_home_g<35":
                    if (row['HTHG'] + row['HTAG']) < 3.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "home", type_rating, points, row["idGame"], row["Date"]])

            for index, row in self.data_team_away.iterrows():
                if type_rating == "dynamic_ft_away":
                    if row['FTHG'] < row['FTAG']:
                        points = 3
                    elif row['FTHG'] == row['FTAG']:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_away_g>15":
                    if (row['FTHG'] + row['FTAG']) > 1.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_away_g>25":
                    if (row['FTHG'] + row['FTAG']) > 2.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_away_g>35":
                    if (row['FTHG'] + row['FTAG']) > 3.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_away_g<15":
                    if (row['FTHG'] + row['FTAG']) < 1.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_away_g<25":
                    if (row['FTHG'] + row['FTAG']) < 2.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_away_g<35":
                    if (row['FTHG'] + row['FTAG']) < 3.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])

                if type_rating == "dynamic_ht_away":
                    if row['HTHG'] < row['HTAG']:
                        points = 3
                    elif row['HTHG'] == row['HTAG']:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_away_g>15":
                    if (row['HTHG'] + row['HTAG']) > 1.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_away_g>25":
                    if (row['HTHG'] + row['HTAG']) > 2.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_away_g>35":
                    if (row['HTHG'] + row['HTAG']) > 3.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_away_g<15":
                    if (row['HTHG'] + row['HTAG']) < 1.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_away_g<25":
                    if (row['HTHG'] + row['HTAG']) < 2.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_away_g<35":
                    if (row['HTHG'] + row['HTAG']) < 3.5:
                        points = 1
                    else:
                        points = 0
                    self.list_rating.append([year, team, "away", type_rating, points, row["idGame"], row["Date"]])

            for index, row in self.data_team_total.iterrows():
                if type_rating == "dynamic_ft_total":
                    if row["AwayTeam"] == team:
                        if row['FTHG'] < row['FTAG']:
                            points = 3
                        elif row['FTHG'] == row['FTAG']:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if row['FTHG'] > row['FTAG']:
                            points = 3
                        elif row['FTHG'] == row['FTAG']:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_total_g>15":
                    if row["AwayTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) > 1.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) > 1.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_total_g>25":
                    if row["AwayTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) > 2.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) > 2.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_total_g>35":
                    if row["AwayTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) > 3.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) > 3.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_total_g<15":
                    if row["AwayTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) < 1.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) < 1.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_total_g<25":
                    if row["AwayTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) < 2.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) < 2.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ft_total_g<35":
                    if row["AwayTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) < 3.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['FTHG'] + row['FTAG']) < 3.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])

                if type_rating == "dynamic_ht_total":
                    if row["AwayTeam"] == team:
                        if row['HTHG'] < row['HTAG']:
                            points = 3
                        elif row['HTHG'] == row['HTAG']:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if row['HTHG'] > row['HTAG']:
                            points = 3
                        elif row['HTHG'] == row['HTAG']:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])

                if type_rating == "dynamic_ht_total_g>15":
                    if row["AwayTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) > 1.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) > 1.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_total_g>25":
                    if row["AwayTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) > 2.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) > 2.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_total_g>35":
                    if row["AwayTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) > 3.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) > 3.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_total_g<15":
                    if row["AwayTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) < 1.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) < 1.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_total_g<25":
                    if row["AwayTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) < 2.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) < 2.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                if type_rating == "dynamic_ht_total_g<35":
                    if row["AwayTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) < 3.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
                    if row["HomeTeam"] == team:
                        if (row['HTHG'] + row['HTAG']) < 3.5:
                            points = 1
                        else:
                            points = 0
                        self.list_rating.append([year, team, "total", type_rating, points, row["idGame"], row["Date"]])
        self.output = None
        self.output = pd.DataFrame(self.list_rating, columns=cons_input.columns_points)

    def __create_rating(self, year: int):
        """
        Calculate rating macro for all the team for each year
        :return:
        """
        for index, row in self.teams.iterrows():
            self.__select_data_team(team=row[cons_path.teams])
            self.__calculate_rating(team=row[cons_path.teams], year=year)
        self.__write_file(year=year)

    def run(self):
        """
        Run the class and create the file with the points for the indicator
        :return:
        """
        start = measure_time(None)
        self.__read_teams()
        for year in list(range(2007, 2020)):
            self.__read_file(year)
            self.__create_rating(year=year)
        print(self.output.head())
        measure_time(start)


for league in cons_path.leagues:
    if league != "GR_super_league":
        print(league)
        dynamic = CreateDynamicsPoints(league=league)
        dynamic.run()
