from src.utils.get_root_path import get_project_root
from src.define_paths import define_path

import src.cons_paths as cons_path
import src.cons_input_data as cons_input
import pandas as pd
import csv

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class CreateRating:

    def __init__(self, league: str):
        self.path = str(get_project_root())
        self.path_dict = define_path(league=league)
        self.stats = pd.DataFrame()
        self.teams = pd.DataFrame()
        self.data_team_total = pd.DataFrame()
        self.data_team_home = pd.DataFrame()
        self.data_team_away = pd.DataFrame()
        self.rating = pd.DataFrame(columns=cons_input.columns_rating)
        self.list_rating = [["year", "team", "type_rating", "value_rating"]]

    def __read_input(self, year: int) -> pd.DataFrame:
        """
        Read file and convert into dataframe
        :param year:
        :return:
        """
        df = pd.read_csv(self.path + self.path_dict.get("path_odds_stats") + cons_path.stats + str(year) +
                         cons_path.csv, sep=",",
                         encoding='unicode_escape', index_col=0)
        df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%Y-%m-%d')
        return df

    def __read_teams(self):
        """
        Read teams file and convert into dataframe
        :return:
        """
        df = pd.read_csv(self.path + self.path_dict.get("path_teams") + cons_path.teams + cons_path.csv, sep=",",
                         encoding='unicode_escape', index_col=0)
        return df

    def __select_data_team(self, team: str) -> None:
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

    def calculate_rating(self, team: str, year: int) -> None:
        """
        Calculate rating for all indicators
        :param team:
        :param year:
        :return:
        """

        for type_rating in cons_input.type_rating[:]:
            total_games = len(self.data_team_total.index)
            total_games_home = len(self.data_team_home.index)
            total_games_away = len(self.data_team_away.index)
            if total_games == 0:
                total_games = 99999999.9
            if total_games_home == 0:
                total_games_home = 99999999.9
            if total_games_away == 0:
                total_games_away = 99999999.9
            if type_rating == "static_ft_total":
                temp_ft_away = len(self.data_team_away.loc[(self.data_team_away['FTAG'] > self.data_team_away[
                    'FTHG'])].index)
                temp_ft_home = len(self.data_team_home.loc[(self.data_team_home['FTHG'] > self.data_team_home[
                    'FTAG'])].index)
                temp_ft_total = temp_ft_away + temp_ft_home
                self.list_rating.append([year, team, type_rating, int((temp_ft_total / total_games) * 1000)])
            elif type_rating == "static_ft_home":
                self.list_rating.append([year, team, type_rating, int((temp_ft_home / total_games_home) * 1000)])
            elif type_rating == "static_ft_away":
                self.list_rating.append([year, team, type_rating, int((temp_ft_away / total_games_away) * 1000)])
                # "year", "team", "type_rating", "value_rating"
            elif type_rating == "static_ft_total_g>15":
                temp_ft_away_g15 = len(self.data_team_away.loc[(self.data_team_away['FTAG'] + self.data_team_away[
                    'FTHG'] > 1.5)].index)
                temp_ft_home_g15 = len(self.data_team_home.loc[(self.data_team_home['FTHG'] + self.data_team_home[
                    'FTAG'] > 1.5)].index)
                temp_ft_total_g15 = temp_ft_away_g15 + temp_ft_home_g15
                self.list_rating.append([year, team, type_rating, int((temp_ft_total_g15 / total_games) * 1000)])
            elif type_rating == "static_ft_home_g>15":
                self.list_rating.append([year, team, type_rating, int((temp_ft_home_g15 / total_games_home) * 1000)])
            elif type_rating == "static_ft_away_g>15":
                self.list_rating.append([year, team, type_rating, int((temp_ft_away_g15 / total_games_away) * 1000)])
            elif type_rating == "static_ft_total_g>25":
                temp_ft_away_g25 = len(self.data_team_away.loc[(self.data_team_away['FTAG'] + self.data_team_away[
                    'FTHG'] > 2.5)].index)
                temp_ft_home_g25 = len(self.data_team_home.loc[(self.data_team_home['FTHG'] + self.data_team_home[
                    'FTAG'] > 2.5)].index)
                temp_ft_total_g25 = temp_ft_away_g25 + temp_ft_home_g25
                self.list_rating.append([year, team, type_rating, int((temp_ft_total_g25 / total_games) * 1000)])
            elif type_rating == "static_ft_home_g>25":
                self.list_rating.append([year, team, type_rating, int((temp_ft_home_g25 / total_games_home) * 1000)])
            elif type_rating == "static_ft_away_g>25":
                self.list_rating.append([year, team, type_rating, int((temp_ft_away_g25 / total_games_away) * 1000)])
            elif type_rating == "static_ft_total_g>35":
                temp_ft_away_g35 = len(self.data_team_away.loc[(self.data_team_away['FTAG'] + self.data_team_away[
                    'FTHG'] > 3.5)].index)
                temp_ft_home_g35 = len(self.data_team_home.loc[(self.data_team_home['FTHG'] + self.data_team_home[
                    'FTAG'] > 3.5)].index)
                temp_ft_total_g35 = temp_ft_away_g35 + temp_ft_home_g35
                self.list_rating.append([year, team, type_rating, int((temp_ft_total_g35 / total_games) * 1000)])
            elif type_rating == "static_ft_home_g>35":
                self.list_rating.append([year, team, type_rating, int((temp_ft_home_g35 / total_games_home) * 1000)])
            elif type_rating == "static_ft_away_g>35":
                self.list_rating.append([year, team, type_rating, int((temp_ft_away_g35 / total_games_away) * 1000)])
            elif type_rating == "static_ft_total_g<15":
                temp_ft_away_g15 = len(self.data_team_away.loc[(self.data_team_away['FTAG'] + self.data_team_away[
                    'FTHG'] < 1.5)].index)
                temp_ft_home_g15 = len(self.data_team_home.loc[(self.data_team_home['FTHG'] + self.data_team_home[
                    'FTAG'] < 1.5)].index)
                temp_ft_total_g15 = temp_ft_away_g15 + temp_ft_home_g15
                self.list_rating.append([year, team, type_rating, int((temp_ft_total_g15 / total_games) * 1000)])
            elif type_rating == "static_ft_home_g<15":
                self.list_rating.append([year, team, type_rating, int((temp_ft_home_g15 / total_games_home) * 1000)])
            elif type_rating == "static_ft_away_g<15":
                self.list_rating.append([year, team, type_rating, int((temp_ft_away_g15 / total_games_away) * 1000)])
            elif type_rating == "static_ft_total_g<25":
                temp_ft_away_g25 = len(self.data_team_away.loc[(self.data_team_away['FTAG'] + self.data_team_away[
                    'FTHG'] < 2.5)].index)
                temp_ft_home_g25 = len(self.data_team_home.loc[(self.data_team_home['FTHG'] + self.data_team_home[
                    'FTAG'] < 2.5)].index)
                temp_ft_total_g25 = temp_ft_away_g25 + temp_ft_home_g25
                self.list_rating.append([year, team, type_rating, int((temp_ft_total_g25 / total_games) * 1000)])
            elif type_rating == "static_ft_home_g<25":
                self.list_rating.append([year, team, type_rating, int((temp_ft_home_g25 / total_games_home) * 1000)])
            elif type_rating == "static_ft_away_g<25":
                self.list_rating.append([year, team, type_rating, int((temp_ft_away_g25 / total_games_away) * 1000)])
            elif type_rating == "static_ft_total_g<35":
                temp_ft_away_g35 = len(self.data_team_away.loc[(self.data_team_away['FTAG'] + self.data_team_away[
                    'FTHG'] < 3.5)].index)
                temp_ft_home_g35 = len(self.data_team_home.loc[(self.data_team_home['FTHG'] + self.data_team_home[
                    'FTAG'] < 3.5)].index)
                temp_ft_total_g35 = temp_ft_away_g35 + temp_ft_home_g35
                self.list_rating.append([year, team, type_rating, int((temp_ft_total_g35 / total_games) * 1000)])
            elif type_rating == "static_ft_home_g<35":
                self.list_rating.append([year, team, type_rating, int((temp_ft_home_g35 / total_games_home) * 1000)])
            elif type_rating == "static_ft_away_g<35":
                self.list_rating.append([year, team, type_rating, int((temp_ft_away_g35 / total_games_away) * 1000)])

            if type_rating == "static_ht_total":
                temp_ht_away = len(self.data_team_away.loc[(self.data_team_away['HTAG'] > self.data_team_away[
                    'HTHG'])].index)
                temp_ht_home = len(self.data_team_home.loc[(self.data_team_home['HTHG'] > self.data_team_home[
                    'HTAG'])].index)
                temp_ht_total = temp_ht_away + temp_ht_home
                self.list_rating.append([year, team, type_rating, int((temp_ht_total / total_games) * 1000)])
            elif type_rating == "static_ht_home":
                self.list_rating.append([year, team, type_rating, int((temp_ht_home / total_games_home) * 1000)])
            elif type_rating == "static_ht_away":
                self.list_rating.append([year, team, type_rating, int((temp_ht_away / total_games_away) * 1000)])
                # "year", "team", "type_rating", "value_rating"
            elif type_rating == "static_ht_total_g>15":
                temp_ht_away_g15 = len(self.data_team_away.loc[(self.data_team_away['HTAG'] + self.data_team_away[
                    'HTHG'] > 1.5)].index)
                temp_ht_home_g15 = len(self.data_team_home.loc[(self.data_team_home['HTHG'] + self.data_team_home[
                    'HTAG'] > 1.5)].index)
                temp_ht_total_g15 = temp_ht_away_g15 + temp_ht_home_g15
                self.list_rating.append([year, team, type_rating, int((temp_ht_total_g15 / total_games) * 1000)])
            elif type_rating == "static_ht_home_g>15":
                self.list_rating.append([year, team, type_rating, int((temp_ht_home_g15 / total_games_home) * 1000)])
            elif type_rating == "static_ht_away_g>15":
                self.list_rating.append([year, team, type_rating, int((temp_ht_away_g15 / total_games_away) * 1000)])
            elif type_rating == "static_ht_total_g>25":
                temp_ht_away_g25 = len(self.data_team_away.loc[(self.data_team_away['HTAG'] + self.data_team_away[
                    'HTHG'] > 2.5)].index)
                temp_ht_home_g25 = len(self.data_team_home.loc[(self.data_team_home['HTHG'] + self.data_team_home[
                    'HTAG'] > 2.5)].index)
                temp_ht_total_g25 = temp_ht_away_g25 + temp_ht_home_g25
                self.list_rating.append([year, team, type_rating, int((temp_ht_total_g25 / total_games) * 1000)])
            elif type_rating == "static_ht_home_g>25":
                self.list_rating.append([year, team, type_rating, int((temp_ht_home_g25 / total_games_home) * 1000)])
            elif type_rating == "static_ht_away_g>25":
                self.list_rating.append([year, team, type_rating, int((temp_ht_away_g25 / total_games_away) * 1000)])
            elif type_rating == "static_ht_total_g>35":
                temp_ht_away_g35 = len(self.data_team_away.loc[(self.data_team_away['HTAG'] + self.data_team_away[
                    'HTHG'] > 3.5)].index)
                temp_ht_home_g35 = len(self.data_team_home.loc[(self.data_team_home['HTHG'] + self.data_team_home[
                    'HTAG'] > 3.5)].index)
                temp_ht_total_g35 = temp_ht_away_g35 + temp_ht_home_g35
                self.list_rating.append([year, team, type_rating, int((temp_ht_total_g35 / total_games) * 1000)])
            elif type_rating == "static_ht_home_g>35":
                self.list_rating.append([year, team, type_rating, int((temp_ht_home_g35 / total_games_home) * 1000)])
            elif type_rating == "static_ht_away_g>35":
                self.list_rating.append([year, team, type_rating, int((temp_ht_away_g35 / total_games_away) * 1000)])
            elif type_rating == "static_ht_total_g<15":
                temp_ht_away_g15 = len(self.data_team_away.loc[(self.data_team_away['HTAG'] + self.data_team_away[
                    'HTHG'] < 1.5)].index)
                temp_ht_home_g15 = len(self.data_team_home.loc[(self.data_team_home['HTHG'] + self.data_team_home[
                    'HTAG'] < 1.5)].index)
                temp_ht_total_g15 = temp_ht_away_g15 + temp_ht_home_g15
                self.list_rating.append([year, team, type_rating, int((temp_ht_total_g15 / total_games) * 1000)])
            elif type_rating == "static_ht_home_g<15":
                self.list_rating.append([year, team, type_rating, int((temp_ht_home_g15 / total_games_home) * 1000)])
            elif type_rating == "static_ht_away_g<15":
                self.list_rating.append([year, team, type_rating, int((temp_ht_away_g15 / total_games_away) * 1000)])
            elif type_rating == "static_ht_total_g<25":
                temp_ht_away_g25 = len(self.data_team_away.loc[(self.data_team_away['HTAG'] + self.data_team_away[
                    'HTHG'] < 2.5)].index)
                temp_ht_home_g25 = len(self.data_team_home.loc[(self.data_team_home['HTHG'] + self.data_team_home[
                    'HTAG'] < 2.5)].index)
                temp_ht_total_g25 = temp_ht_away_g25 + temp_ht_home_g25
                self.list_rating.append([year, team, type_rating, int((temp_ht_total_g25 / total_games) * 1000)])
            elif type_rating == "static_ht_home_g<25":
                self.list_rating.append([year, team, type_rating, int((temp_ht_home_g25 / total_games_home) * 1000)])
            elif type_rating == "static_ht_away_g<25":
                self.list_rating.append([year, team, type_rating, int((temp_ht_away_g25 / total_games_away) * 1000)])
            elif type_rating == "static_ht_total_g<35":
                temp_ht_away_g35 = len(self.data_team_away.loc[(self.data_team_away['HTAG'] + self.data_team_away[
                    'HTHG'] < 3.5)].index)
                temp_ht_home_g35 = len(self.data_team_home.loc[(self.data_team_home['HTHG'] + self.data_team_home[
                    'HTAG'] < 3.5)].index)
                temp_ht_total_g35 = temp_ht_away_g35 + temp_ht_home_g35
                self.list_rating.append([year, team, type_rating, int((temp_ht_total_g35 / total_games) * 1000)])
            elif type_rating == "static_ht_home_g<35":
                self.list_rating.append([year, team, type_rating, int((temp_ht_home_g35 / total_games_home) * 1000)])
            elif type_rating == "static_ht_away_g<35":
                self.list_rating.append([year, team, type_rating, int((temp_ht_away_g35 / total_games_away) * 1000)])

    def __write_output(self) -> None:
        with open(self.path + self.path_dict.get("path_rating_macro") + cons_path.rating_macro + cons_path.csv, "w",
                  newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.list_rating)

    def __create_rating(self, year: int):
        """
        Calculate rating macro for all the team for each year
        :return:
        """
        for index, row in self.teams.iterrows():
            self.__select_data_team(team=row[cons_path.teams])
            self.calculate_rating(team=row[cons_path.teams], year=year)
        print(self.list_rating)

    def run_rating(self, init_year: int, end_year: int):
        self.teams = self.__read_teams()
        for year in list(range(init_year, end_year)):
            self.stats = self.__read_input(year=year)
            self.__create_rating(year=year)
            self.__write_output()
