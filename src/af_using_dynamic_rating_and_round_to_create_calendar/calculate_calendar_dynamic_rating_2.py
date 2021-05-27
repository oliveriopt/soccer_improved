# TODO:
# a) Write the file to calendar with rating
# b) MAke the division between leters
# c) Start to think to the backtest
# d) Start to think about bayesian test

from src.utils.get_root_path import get_project_root
from src.define_paths import define_path
from datetime import datetime, timedelta, date

import src.cons_input_data as cons_input
import src.cons_paths as cons_path
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class JoinData:

    def __init__(self, league: str):
        self.path = str(get_project_root())
        self.path_dict = define_path(league=league)
        self.calendar = pd.DataFrame()
        self.teams = None
        self.rating = pd.DataFrame()

    def __read_files(self, year: int) -> None:
        """
        Read the file with the rating fixo macro and rating_dynamic
        :param year:
        :return:
        """
        self.calendar = pd.read_csv(self.path + self.path_dict.get("path_calendar") +
                                    cons_path.calendar + "_" + str(year) + cons_path.csv, sep=",", encoding=
                                    'unicode_escape')
        self.teams = list(set(self.calendar["team"].tolist()))
        self.teams.sort()

    def __calculate_rating_dynamic_after_game(self):
        #print(self.teams)
        self.rating = pd.DataFrame()
        for team in self.teams[:]:
            #print(team)
            df_temp = self.calendar[self.calendar["team"] == team].reset_index(drop=True)
            df_temp_total = None
            df_temp_home = None
            df_temp_away = None
            for type_rating in cons_input.type_rating_dynamic[:]:
                if type_rating[11:15] == "tota":
                    df_temp_total = df_temp[df_temp["type_rating"] == type_rating[8:]].reset_index(drop=True)
                    df_temp_total["sum_points"] = df_temp_total["points"].cumsum()

                    df_temp_total["rating_dynamic"] = df_temp_total["Rating_Initial"] * (
                            1 - df_temp_total["Round_as_Total"] /
                            df_temp_total["Round_as_Total"].iloc[-1])
                    df_temp_total["rating_dynamic"] = df_temp_total["rating_dynamic"] + ((df_temp_total["sum_points"] /
                                                                                          df_temp_total[
                                                                                              "Round_as_Total"].iloc[
                                                                                              -1]) * 1000)
                    self.rating = self.rating.append(df_temp_total)
                if type_rating[11:15] == "home":
                    df_temp_home = df_temp[df_temp["type_rating"] == type_rating[8:]].reset_index(drop=True)
                    df_temp_home["sum_points"] = df_temp_home["points"].cumsum()

                    df_temp_home["rating_dynamic"] = df_temp_home["Rating_Initial"] * (
                            1 - df_temp_home["Round_as_Home"] /
                            df_temp_home["Round_as_Home"].iloc[-1])
                    df_temp_home["rating_dynamic"] = df_temp_home["rating_dynamic"] + ((df_temp_home["sum_points"] /
                                                                                        df_temp_home[
                                                                                            "Round_as_Home"].iloc[
                                                                                            -1]) * 1000)
                    self.rating = self.rating.append(df_temp_home)
                if type_rating[11:15] == "away":
                    df_temp_away = df_temp[df_temp["type_rating"] == type_rating[8:]].reset_index(drop=True)
                    df_temp_away["sum_points"] = df_temp_away["points"].cumsum()

                    df_temp_away["rating_dynamic"] = df_temp_away["Rating_Initial"] * (
                            1 - df_temp_away["Round_as_Away"] /
                            df_temp_away["Round_as_Away"].iloc[-1])
                    df_temp_away["rating_dynamic"] = df_temp_away["rating_dynamic"] + ((df_temp_away["sum_points"] /
                                                                                        df_temp_away[
                                                                                            "Round_as_Away"].iloc[
                                                                                            -1]) * 1000)
                    self.rating = self.rating.append(df_temp_away)

        self.rating = self.rating.reset_index(drop=True)
        #print(self.rating)


    def __write_file(self, year: int):
        self.rating.columns = self.rating.columns.str.lower()
        self.rating["rating_dynamic"] = self.rating["rating_dynamic"].astype(int)
        self.rating.to_csv(self.path + self.path_dict.get("path_calendar") +
                           cons_path.calendar + "_dynamic_" + str(year) + cons_path.csv, index=False)
        print(self.rating)

    def run(self):
        """

        :return:
        """
        for year in list(range(2007, 2021)):
            print(year)
            self.__read_files(year=year)
            # print(self.calendar)
            self.__calculate_rating_dynamic_after_game()
            self.__write_file(year=year)
        #print(self.rating)

for league in cons_path.leagues[:1]:
    if league != "GR_super_league":
        print(league)
        join_data = JoinData(league=league)
        join_data.run()
